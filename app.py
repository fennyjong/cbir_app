from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os
from PIL import Image  # Importing PIL to handle image resizing
from config import Config
from models import db, User, SongketDataset

app = Flask(__name__)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create upload directory if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already registered!', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':
            session['user_role'] = 'admin'
            return redirect(url_for('dashboard_admin'))
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            user.last_login_at = db.func.now()  # Update last login time
            db.session.commit()  # Save changes
            session['user_role'] = 'user'
            return redirect(url_for('modul_upload'))
        
    return render_template('auth/login.html')

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')

    user = User.query.filter_by(username=username).first()
    if user:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"success": True, "message": "Password reset successful."}), 200
    return jsonify({"success": False, "message": "Username not found."}), 404

@app.route('/dashboard_admin')
def dashboard_admin():
    if session.get('user_role') != 'admin':
        flash('You do not have access to this page.', 'danger')
        return redirect(url_for('login'))
    return render_template('admin/dashboard_admin.html')

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    session.pop('user_role', None)
    return jsonify({"success": True, "message": "You have been logged out successfully."})

@app.route('/new_dataset')
def new_dataset():
    return render_template('admin/new_dataset.html')

@app.route('/users/modul_upload', methods=['GET'])
@login_required
def modul_upload():
    return render_template('users/modul_upload.html')

@app.route('/upload', methods=['POST'])
def upload():
    if session.get('user_role') != 'admin':
        flash('You do not have permission to upload.', 'danger')
        return redirect(url_for('login'))
    
    region = request.form['region']
    fabric_name = request.form['fabric_name']
    image = request.files['image']
    
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        save_dir = os.path.join(app.config['UPLOAD_FOLDER'])
        
        # Open image using PIL and resize it to 255x255
        img = Image.open(image)
        img_resized = img.resize((255, 255))  # Resize to 255x255
        
        # Save resized image
        img_resized.save(os.path.join(save_dir, filename))
        
        # Save dataset info to the database
        new_dataset = SongketDataset(region=region, fabric_name=fabric_name, image_filename=filename)
        db.session.add(new_dataset)
        db.session.commit()
        
        flash('Dataset added successfully with resized image!', 'success')
    else:
        flash('Image not found or invalid file type!', 'danger')
    
    return redirect(url_for('dashboard_admin'))

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/get_datasets', methods=['GET'])
def get_datasets():
    datasets = SongketDataset.query.all()
    return jsonify([{
        'id': dataset.id,
        'region': dataset.region,
        'fabric_name': dataset.fabric_name,
        'image_filename': dataset.image_filename
    } for dataset in datasets])

@app.route('/edit_dataset', methods=['POST'])
def edit_dataset():
    data = request.json
    dataset = SongketDataset.query.get(data['id'])
    if dataset:
        dataset.fabric_name = data['fabric_name']
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Dataset not found'}), 404

@app.route('/delete_dataset', methods=['POST'])
def delete_dataset():
    data = request.json
    dataset = SongketDataset.query.get(data['id'])
    if dataset:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], dataset.image_filename))
        db.session.delete(dataset)
        db.session.commit()
        return jsonify({'success': True}), 200
    return jsonify({'success': False, 'message': 'Dataset not found'}), 404

@app.route('/delete_multiple_datasets', methods=['POST'])
def delete_multiple_datasets():
    ids = request.json.get('ids', [])
    success = True
    
    for id in ids:
        dataset = SongketDataset.query.get(id)
        if dataset:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], dataset.image_filename))
            db.session.delete(dataset)
        else:
            success = False
    
    db.session.commit()
    return jsonify({'success': success})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
