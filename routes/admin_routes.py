from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session, send_from_directory
from flask_login import login_required
from models import db, SongketDataset, Label, User, SearchHistory
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
from PIL import Image
from proses.augmentasi import augment_image
from proses.train_model import CBIRModel, get_last_processing_time

admin_bp = Blueprint('admin', __name__)

from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models import db, SongketDataset, Label, User, DailyStats
from sqlalchemy import func, extract
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/dashboard')
def dashboard_admin():
    if session.get('user_role') != 'admin':
        flash('You need admin privileges to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('admin/dashboard_admin.html')

from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from models import db, SongketDataset, Label, User, DailyStats
from sqlalchemy import func, extract, and_
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard_admin():
    if session.get('user_role') != 'admin':
        flash('You need admin privileges to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('admin/dashboard_admin.html')

@admin_bp.route('/api/stats/<timeframe>')
def get_stats(timeframe):
    today = datetime.now().date()
    
    if timeframe == 'daily':
        # Last 30 days
        start_date = today - timedelta(days=30)
        date_format = '%Y-%m-%d'
        date_extract = func.date(User.created_at)
        group_by = date_extract
        
    elif timeframe == 'monthly':
        # Last 12 months
        start_date = today - timedelta(days=365)
        date_format = '%Y-%m'
        date_extract = func.date_trunc('month', User.created_at)
        group_by = date_extract
        
    elif timeframe == 'yearly':
        # Last 5 years
        start_date = today - timedelta(days=1825)
        date_format = '%Y'
        date_extract = extract('year', User.created_at)
        group_by = date_extract
    else:
        return jsonify({'error': 'Invalid timeframe'}), 400

    # Calculate total datasets
    total_datasets = db.session.query(SongketDataset).count()

    # Calculate total registrations (all time)
    total_registrations = db.session.query(User).count()

    # Calculate total logins (for the selected period)
    total_logins = db.session.query(User).filter(
        User.last_login_at >= start_date
    ).count()

    # Get registrations over time
    registrations = db.session.query(
        group_by.label('date'),
        func.count(User.id).label('count')
    ).filter(
        User.created_at >= start_date
    ).group_by(group_by).all()

    # Get logins over time
    logins = db.session.query(
        func.date_trunc(timeframe, User.last_login_at).label('date'),
        func.count(User.id).label('count')
    ).filter(
        User.last_login_at >= start_date
    ).group_by('date').all()

    # Get datasets over time
    datasets = db.session.query(
        func.date_trunc(timeframe, SongketDataset.uploaded_at).label('date'),
        func.count(SongketDataset.id).label('count')
    ).filter(
        SongketDataset.uploaded_at >= start_date
    ).group_by('date').all()

    # Format the data
    reg_data = {str(date.strftime(date_format) if hasattr(date, 'strftime') else date): count 
                for date, count in registrations}
    login_data = {str(date.strftime(date_format) if hasattr(date, 'strftime') else date): count 
                  for date, count in logins}
    dataset_data = {str(date.strftime(date_format) if hasattr(date, 'strftime') else date): count 
                    for date, count in datasets}

    return jsonify({
        'registrations': reg_data,
        'logins': login_data,
        'datasets': dataset_data,
        'totals': {
            'total_datasets': total_datasets,
            'total_registrations': total_registrations,
            'total_logins': total_logins
        }
    })

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

from datetime import datetime

@admin_bp.route('/upload', methods=['POST'])
def upload():
    if session.get('user_role') != 'admin':
        flash('You do not have permission to upload.', 'danger')
        return redirect(url_for('login'))

    region = request.form['region']
    fabric_name = request.form['label_name']
    image = request.files['image']
    cropped_data = request.form.get('cropped-data')

    if image and allowed_file(image.filename) and cropped_data:
        # Generate a unique filename using a timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(f"{fabric_name}_{region}_{timestamp}.png")
        save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

        # Process the cropped image data
        cropped_data = cropped_data.split(',')[1]
        img_data = base64.b64decode(cropped_data)
        img = Image.open(BytesIO(img_data))

        # Resize the cropped image if necessary
        img_resized = img.resize((255, 255))
        img_resized.save(save_path)

        try:
            # Check if the augment checkbox is checked
            augment = request.form.get('augment') == 'on'

            # Perform augmentation if checked
            if augment:
                output_folder = current_app.config['UPLOAD_FOLDER']

                augmented_files = augment_image(save_path, output_folder)

                # Save augmented images to database
                for aug_file in augmented_files:
                    aug_filename = os.path.basename(aug_file)
                    new_dataset = SongketDataset(region=region, fabric_name=fabric_name, image_filename=aug_filename)
                    db.session.add(new_dataset)

                flash('Gambar berhasil diunggah dengan augmentasi', 'success')
            else:
                # Save original dataset information
                new_dataset = SongketDataset(region=region, fabric_name=fabric_name, image_filename=filename)
                db.session.add(new_dataset)
                flash('Gambar berhasil diunggah tanpa augmentasi.', 'success')

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f'Terjadi kesalahan saat menyimpan data: {str(e)}', 'danger')
            current_app.logger.error(f'Database error: {str(e)}')
    else:
        flash('Gambar tidak ditemukan atau jenis file tidak valid', 'danger')

    return redirect(url_for('admin.new_dataset_view'))


@admin_bp.route('/new_dataset')
def new_dataset_view():
    # Query data nama kain dan daerah asal dari database
    labels = db.session.query(Label).all()  # Ambil semua objek Label
    regions = db.session.query(Label.region).distinct().all()  # Ambil daerah asal unik

    # Mengubah data menjadi Fabric Name format
    fabric_names = [label.fabric_name for label in labels]  # Ambil nama kain sebagai list
    unique_regions = [region[0] for region in regions]  # Ambil daerah asal unik sebagai list

    # Render template dengan data yang diperlukan
    return render_template('admin/new_dataset.html', fabric_names=fabric_names, regions=unique_regions)

# Add these imports at the top of your admin_bp file
from flask import send_file
import csv
from io import StringIO
from sqlalchemy import or_
from datetime import datetime
import math

<<<<<<< HEAD
=======
@admin_bp.route('/search-history')
@login_required
def search_history():
    if session.get('user_role') != 'admin':
        flash('You need admin privileges to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('admin/search_history.html')

@admin_bp.route('/api/search-history')
@login_required
def get_search_history():
    if session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search_query = request.args.get('search', '')
    
    # Base query
    query = db.session.query(
        SearchHistory, User.username
    ).join(
        User, SearchHistory.user_id == User.id
    )
    
    # Apply search filter if provided
    if search_query:
        query = query.filter(
            or_(
                User.username.ilike(f'%{search_query}%'),
                SearchHistory.query_image.ilike(f'%{search_query}%')
            )
        )
    
    # Get total count for pagination
    total_count = query.count()
    
    # Apply pagination
    query = query.order_by(SearchHistory.search_timestamp.desc())\
                .offset((page - 1) * per_page)\
                .limit(per_page)
    
    # Format results
    results = []
    for history, username in query.all():
        results.append({
            'id': history.id,
            'username': username,
            'query_image': history.query_image,
            'timestamp': history.search_timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({
        'success': True,
        'data': results,
        'total': total_count,
        'pages': math.ceil(total_count / per_page),
        'current_page': page
    })

@admin_bp.route('/api/search-history/delete/<int:history_id>', methods=['DELETE'])
@login_required
def delete_search_history(history_id):
    if session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        history_entry = SearchHistory.query.get_or_404(history_id)
        db.session.delete(history_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Search history deleted successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error deleting search history: {str(e)}'
        }), 500

@admin_bp.route('/api/search-history/clear', methods=['DELETE'])
@login_required
def clear_search_history():
    if session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        SearchHistory.query.delete()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'All search history cleared successfully'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error clearing search history: {str(e)}'
        }), 500

@admin_bp.route('/api/search-history/export')
@login_required
def export_search_history():
    if session.get('user_role') != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    try:
        # Query all search history with usernames
        history_data = db.session.query(
            SearchHistory, User.username
        ).join(
            User, SearchHistory.user_id == User.id
        ).order_by(
            SearchHistory.search_timestamp.desc()
        ).all()
        
        # Create CSV in memory
        si = StringIO()
        writer = csv.writer(si)
        writer.writerow(['No.', 'Username', 'Query Image', 'Timestamp'])
        
        for i, (history, username) in enumerate(history_data, 1):
            writer.writerow([
                i,
                username,
                history.query_image,
                history.search_timestamp.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        output = si.getvalue()
        si.close()
        
        # Create response
        return send_file(
            StringIO(output),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'search_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error exporting search history: {str(e)}'
        }), 500

>>>>>>> 66c8319c7f861e08bf1a2a6f56fe4beed2b85c06
@admin_bp.route('/process_database', methods=['POST'])
def process_database():
    if session.get('user_role') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized access'
        }), 401

    try:
        cbir = CBIRModel(
            upload_folder=current_app.config['UPLOAD_FOLDER'],
            features_path='model/features.h5'
        )
        
        success, message = cbir.process_database()
        
        if success:
            last_processing = get_last_processing_time()
            return jsonify({
                'success': True,
                'message': message,
                'timestamp': last_processing
            })
        else:
            return jsonify({
                'success': False,
                'message': message
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Processing failed: {str(e)}'
        })

@admin_bp.route('/search_similar', methods=['POST'])
def search_similar():
    if 'image' not in request.files:
        return jsonify({
            'success': False,
            'message': 'No image file provided'
        })

    try:
        image = request.files['image']
        
        # Save temporary file
        temp_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'temp_query.jpg')
        image.save(temp_path)

        # Initialize CBIR model
        cbir = CBIRModel(
            upload_folder=current_app.config['UPLOAD_FOLDER'],
            features_path='model/features.h5'
        )

        # Search for similar images
        results = cbir.search_similar(temp_path, top_k=5)
        
        # Remove temporary file
        os.remove(temp_path)

        if results is None:
            return jsonify({
                'success': False,
                'message': 'Error processing query image'
            })

        return jsonify({
            'success': True,
            'results': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Search failed: {str(e)}'
        })

@admin_bp.route('/get_last_processing', methods=['GET'])
def get_last_processing():
    timestamp = get_last_processing_time()
    return jsonify({
        'timestamp': timestamp
    })