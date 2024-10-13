from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, User, SongketDataset
from werkzeug.utils import secure_filename
from flask import Flask, session
import os

app = Flask(__name__)
app.config.from_object(Config)  # Menggunakan konfigurasi dari kelas Config
db.init_app(app)  # Inisialisasi SQLAlchemy dengan app

# Route untuk halaman utama
@app.route('/')
def home():
    return render_template('login.html')

# Route untuk registrasi pengguna
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Periksa apakah username sudah ada
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username sudah terdaftar!', 'danger')
            return redirect(url_for('register'))

        # Buat pengguna baru dengan password ter-hash
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Route untuk login pengguna
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        # Cek kredensial admin
        if username == 'admin' and password == 'admin':
            return redirect(url_for('dashboard_admin'))
        elif user and user.check_password(password):
            return redirect(url_for('dashboard_user'))
        else:
            flash('Username atau password salah!', 'danger')

    return render_template('login.html')

# Route untuk dashboard admin
@app.route('/dashboard_admin', methods=['GET'])
def dashboard_admin():
    return render_template('dashboard_admin.html')

# Route untuk upload dataset
@app.route('/upload', methods=['POST'])
def upload():
    region = request.form['region']
    fabric_name = request.form['fabric_name']
    image = request.files['image']

    if image:
        filename = secure_filename(image.filename)
        save_dir = os.path.join(os.getcwd(), 'uploads')  # Save images in uploads folder

        # Create the directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Save the image
        image.save(os.path.join(save_dir, filename))

        # Menyimpan informasi ke database
        new_dataset = SongketDataset(region=region, fabric_name=fabric_name, image_filename=filename)
        db.session.add(new_dataset)
        db.session.commit()

        flash('Dataset berhasil ditambahkan!', 'success')
    else:
        flash('Gambar tidak ditemukan!', 'danger')

    return redirect(url_for('dashboard_admin'))

# Route untuk dashboard pengguna (jika ada)
@app.route('/dashboard_user')
def dashboard_user():
    return render_template('dashboard_user.html')

@app.route('/logout')
def logout():
    session.pop('user', None)  # Remove the user from the session
    return redirect(url_for('login'))  # Redirect to the login page

if __name__ == '__main__':
    with app.app_context():  # Set up application context
        db.create_all()  # Buat tabel jika belum ada
    app.run(debug=True)
