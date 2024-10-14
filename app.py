from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cbir_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SongketDataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    fabric_name = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(200), nullable=False)

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
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username sudah terdaftar!', 'danger')
            return redirect(url_for('register'))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':
            session['user_role'] = 'admin'
            flash('Login admin berhasil!', 'success')
            return redirect(url_for('dashboard_admin'))
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            session['user_role'] = 'user'
            flash('Login berhasil!', 'success')
            return redirect(url_for('dashboard_user'))
        else:
            flash('Username atau password salah!', 'danger')
    
    return render_template('login.html')

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.get_json()
    username = data.get('username')
    new_password = data.get('new_password')

    user = User.query.filter_by(username=username).first()
    if user:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({"success": True, "message": "Password berhasil direset."}), 200
    else:
        return jsonify({"success": False, "message": "Username tidak ditemukan."}), 404

@app.route('/dashboard_admin')
def dashboard_admin():
    if session.get('user_role') != 'admin':
        flash('Anda tidak memiliki akses ke halaman ini.', 'danger')
        return redirect(url_for('login'))
    return render_template('dashboard_admin.html')

@app.route('/dashboard_user')
@login_required
def dashboard_user():
    return render_template('dashboard_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_role', None)
    flash('Anda telah berhasil logout.', 'success')
    return redirect(url_for('login'))

@app.route('/upload', methods=['POST'])
def upload():
    if session.get('user_role') != 'admin':
        flash('Anda tidak memiliki akses untuk melakukan upload.', 'danger')
        return redirect(url_for('login'))
    
    region = request.form['region']
    fabric_name = request.form['fabric_name']
    image = request.files['image']
    
    if image:
        filename = secure_filename(image.filename)
        save_dir = os.path.join(app.config['UPLOAD_FOLDER'])
        
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        image.save(os.path.join(save_dir, filename))
        
        new_dataset = SongketDataset(region=region, fabric_name=fabric_name, image_filename=filename)
        db.session.add(new_dataset)
        db.session.commit()
        
        flash('Dataset berhasil ditambahkan!', 'success')
    else:
        flash('Gambar tidak ditemukan!', 'danger')
    
    return redirect(url_for('dashboard_admin'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)