from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session, send_from_directory
from flask_login import login_required
from models import db, SongketDataset, SearchHistory, Label
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
from PIL import Image
from proses.augmentasi import augment_image
from proses.train_model import CBIRModel, get_last_processing_time
from flask import Blueprint, jsonify, send_file
from datetime import datetime
import csv
import io

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
def dashboard_admin():
    if session.get('user_role') != 'admin':
        flash('You need admin privileges to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard_admin.html')

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

@admin_bp.route('/process_database', methods=['POST'])
def process_database():
    if session.get('user_role') != 'admin':
        return jsonify({
            'success': False,
            'message': 'Unauthorized access'
        }), 401

    try:
        cbir = CBIRModel(
            upload_folder=current_app.config['UPLOAD_FOLDER']
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
    
@admin_bp.route('/get_last_processing', methods=['GET'])
def get_last_processing():
    timestamp = get_last_processing_time()
    return jsonify({
        'timestamp': timestamp
    })

def generate_csv(history_records):
    output = io.StringIO()
    writer = csv.writer(output)

    # Write the header
    writer.writerow(['ID', 'Username', 'Query Image', 'Timestamp'])

    # Write each record
    for record in history_records:
        writer.writerow([record.id, record.user.username, record.query_image, record.search_timestamp.strftime('%Y-%m-%d %H:%M:%S')])

    output.seek(0)
    return output

@admin_bp.route('/api/search_history', methods=['GET'])
def view_search_history():
    history_records = SearchHistory.query.all()
    csv_output = generate_csv(history_records)
    
    if 'export' in request.args:
        return send_file(io.BytesIO(csv_output.getvalue().encode('utf-8')),
                         as_attachment=True,
                         download_name='search_history.csv',
                         mimetype='text/csv')
    
    return csv_output.getvalue(), 200, {'Content-Type': 'text/csv'}
@admin_bp.route('/edit_dataset/<int:id>', methods=['GET', 'POST'])
def edit_dataset_page(id):
    dataset = SongketDataset.query.get_or_404(id)
    
    # Mengambil data dari tabel Label untuk dropdown
    fabric_data = db.session.query(Label.fabric_name, Label.region).distinct().order_by(Label.fabric_name).all()
    
    # Konversi ke dictionary untuk kemudahan akses di template
    fabric_regions = {fabric: region for fabric, region in fabric_data}
    fabric_names = list(fabric_regions.keys())

    # Jika form di-submit, update dataset
    if request.method == 'POST':
        fabric_name = request.form.get('label_name')
        region = request.form.get('region')

        # Update dataset
        dataset.fabric_name = fabric_name
        dataset.region = region
        try:
            db.session.commit()
            flash('Dataset berhasil diperbarui!', 'success')  # Flash success message
            return redirect(url_for('admin_bp.edit_dataset_page', id=id))  # Redirect back to the same page to trigger pop-up
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('admin_bp.edit_dataset_page', id=id))  # Redirect back if error

    return render_template('admin/edit_dataset.html', 
                           dataset=dataset, 
                           fabric_names=fabric_names,
                           fabric_regions=fabric_regions)

@admin_bp.route('/api/update_dataset/<int:id>', methods=['POST'])
def update_dataset(id):
    data = request.get_json()
    fabric_name = data.get('fabric_name')
    region = data.get('region')

    # Validate or process the data and update the dataset
    # Example: Update dataset in database
    dataset = SongketDataset.query.get(id)
    if dataset:
        dataset.fabric_name = fabric_name
        dataset.region = region
        db.session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False, message="Dataset not found"), 404
