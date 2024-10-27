from flask import Blueprint, render_template, request, current_app, url_for, redirect
from flask_login import login_required
from models import db, Label, SongketDataset
from werkzeug.utils import secure_filename
import os

user_bp = Blueprint('user', __name__)

# Add this to handle allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'query_image' not in request.files:
            return redirect(url_for('user.upload'))
        
        file = request.files['query_image']
        if file.filename == '':
            return redirect(url_for('user.upload'))
        
        if file and allowed_file(file.filename):
            # Generate unique filename to prevent overwrites
            filename = secure_filename(file.filename)
            # Ensure upload folder exists
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save the file
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)
            
            # Get the URL for the uploaded image
            image_url = url_for('static', filename=f'uploads/{filename}')
            
            # Here you would typically:
            # 1. Process the image
            # 2. Compare with database
            # 3. Get similar songket images
            
            # For now, we'll just pass the uploaded image
            similar_results = []  # This would be populated with your similarity search results
            
            return render_template('users/modul_hasil.html',
                                query_image=image_url,
                                n_results=int(request.args.get('n_results', 10)),
                                results=similar_results)
    
    # Handle GET request
    return render_template('users/modul_hasil.html',
                         query_image=request.args.get('query_image', ''),
                         n_results=int(request.args.get('n_results', 10)),
                         results=[])

@user_bp.route('/panduan')
@login_required
def panduan():
    return render_template('users/panduan.html')

@user_bp.route('/informasi')
@login_required
def display_songket():
    # Join between SongketDataset and Label to get unique songket data with labels
    songkets_with_labels = db.session.query(SongketDataset, Label).\
        join(Label, SongketDataset.fabric_name == Label.fabric_name).\
        distinct(SongketDataset.fabric_name).all()

    # Check if data is available
    if not songkets_with_labels:
        error = "Tidak ada songket yang tersedia saat ini."
        return render_template('users/modul_informasi.html', error=error)

    # Return template with songket and label data
    return render_template('users/modul_informasi.html', songkets_with_labels=songkets_with_labels)