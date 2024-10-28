from flask import Blueprint, render_template, request, current_app, url_for, redirect
from flask_login import login_required, current_user
from models import db, SearchHistory, Label, SongketDataset
from werkzeug.utils import secure_filename
import os
from datetime import datetime
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
            # Generate unique filename
            filename = secure_filename(file.filename)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S_')
            unique_filename = timestamp + filename
            
            # Ensure upload folder exists
            upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save the file
            filepath = os.path.join(upload_folder, unique_filename)
            file.save(filepath)
            
            # Get the URL for the uploaded image
            image_url = url_for('static', filename=f'uploads/{unique_filename}')
            
            # Save to search_history table
            search_history = SearchHistory(
                user_id=current_user.id,
                query_image=unique_filename,
                search_timestamp=datetime.utcnow()
            )
            
            try:
                db.session.add(search_history)
                db.session.commit()
                print(f"Successfully saved search history for user {current_user.username}")
            except Exception as e:
                print(f"Error saving to database: {str(e)}")
                db.session.rollback()
            
            similar_results = []  # This would be populated with your similarity search results
            
            return render_template('users/modul_hasil.html',
                                query_image=image_url,
                                n_results=int(request.args.get('n_results', 10)),
                                results=similar_results)
    
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