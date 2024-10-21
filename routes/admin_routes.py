from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, session, send_from_directory
from flask_login import login_required
from models import db, SongketDataset, Label
from werkzeug.utils import secure_filename
import os
import base64
from io import BytesIO
from PIL import Image
from proses.augmentasi import augment_image

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
