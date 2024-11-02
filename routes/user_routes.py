from flask import Blueprint, render_template, request, current_app, url_for, redirect, send_from_directory, jsonify
from flask_login import login_required, current_user
from models import db, SearchHistory
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from proses.cosine import CBIRModel
from models import SongketDataset, SongketFeatures, Label
import shutil

user_bp = Blueprint('user', __name__)

# Initialize CBIR model
cbir_model = None

def get_cbir_model():
    global cbir_model
    if cbir_model is None:
        from proses.cosine import CBIRModel
        upload_folder = os.path.join(current_app.root_path, 'uploads')
        cbir_model = CBIRModel(upload_folder=upload_folder)
    return cbir_model

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.route('/uploads/<filename>')
def serve_upload(filename):
    upload_folder = os.path.join(current_app.root_path, 'uploads')
    return send_from_directory(upload_folder, filename)

@user_bp.route('/beranda')
@login_required
def beranda():
    return render_template('users/beranda.html')

@user_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    return render_template('users/modul_upload.html')

@user_bp.route('/hasil', methods=['GET', 'POST'])
@login_required
def hasil():
    model = get_cbir_model()
    
    if request.method == 'POST':
        if 'query_image' not in request.files:
            return redirect(url_for('user.upload'))
        
        file = request.files['query_image']
        if file.filename == '' or not allowed_file(file.filename):
            return redirect(url_for('user.upload'))

        filename = secure_filename(file.filename)
        static_uploads = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(static_uploads, exist_ok=True)
        static_filepath = os.path.join(static_uploads, filename)
        file.save(static_filepath)

        image_url = url_for('static', filename=f'uploads/{filename}')
        
        # Ekstrak fitur dari gambar query
        query_features = model.extract_features(static_filepath)
        if query_features is None:
            return "Error processing image", 400
        
        # Dapatkan jumlah hasil pencarian yang diminta
        try:
            n_results = int(request.form.get('count', 10))
            if n_results <= 0:
                n_results = 10
        except (TypeError, ValueError):
            n_results = 10
            
        # Cari gambar yang mirip dan ambil detail tambahan
        similar_results = model.find_similar_images(query_features, n_results)
        
        # Simpan riwayat pencarian
        search_history = SearchHistory(
            user_id=current_user.id,
            query_image=filename,
            search_timestamp=datetime.utcnow()
        )
        
        try:
            db.session.add(search_history)
            db.session.commit()
        except Exception as e:
            print(f"Error saving search history: {str(e)}")
            db.session.rollback()
            return "Error saving search history", 500

        # Jika permintaan AJAX, kembalikan JSON
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({
                'results': similar_results
            })

        # Tampilkan hasil dengan nama kain dan asal daerah
        return render_template('users/modul_hasil.html',
                             query_image=image_url,
                             n_results=n_results,
                             results=similar_results)
    
    # (Kode untuk handle GET request tetap sama)
    try:
        n_results = int(request.args.get('count', 10))
        if n_results <= 0:
            n_results = 10
    except (TypeError, ValueError):
        n_results = 10
        
    query_image = request.args.get('query_image', '')
    
    if query_image:
        static_filepath = os.path.join(current_app.root_path, 'static', 'uploads', 
                                     os.path.basename(query_image))
        if os.path.exists(static_filepath):
            query_features = model.extract_features(static_filepath)
            similar_results = model.find_similar_images(query_features, n_results)
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({
                    'results': similar_results
                })
                
            query_image = url_for('static', filename=f'uploads/{os.path.basename(query_image)}')
        else:
            similar_results = []
    else:
        similar_results = []
        
    return render_template('users/modul_hasil.html',
                         query_image=query_image,
                         n_results=n_results,
                         results=similar_results)

@user_bp.route('/panduan')
@login_required
def panduan():
    return render_template('users/panduan.html')

@user_bp.route('/informasi')
@login_required
def display_songket():
    songkets_with_labels = db.session.query(SongketDataset, Label).\
        join(Label, SongketDataset.fabric_name == Label.fabric_name).\
        distinct(SongketDataset.fabric_name).all()

    if not songkets_with_labels:
        error = "Tidak ada songket yang tersedia saat ini."
        return render_template('users/modul_informasi.html', error=error)

    return render_template('users/modul_informasi.html', songkets_with_labels=songkets_with_labels)