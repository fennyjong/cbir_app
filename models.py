from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi ekstensi
db = SQLAlchemy()  # Inisialisasi SQLAlchemy untuk database
bcrypt = Bcrypt()  # Inisialisasi Bcrypt untuk hashing password

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Nama tabel di database
    id = db.Column(db.Integer, primary_key=True)  # ID unik untuk pengguna
    username = db.Column(db.String(80), unique=True, nullable=False)  # Nama pengguna unik
    password_hash = db.Column(db.String(255), nullable=False)  # Hash password
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # Waktu pendaftaran
    last_login_at = db.Column(db.DateTime, nullable=True)  # Waktu login terakhir

    def set_password(self, password):
        """Mengatur password dan hash-nya."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Memeriksa kecocokan password dengan hash."""
        return check_password_hash(self.password_hash, password)

class SongketDataset(db.Model):
    __tablename__ = 'songket_dataset'
    
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(100), nullable=False)
    fabric_name = db.Column(db.String(100), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<SongketDataset {self.fabric_name} from {self.region}>'

class Label(db.Model):
    __tablename__ = 'labels'  # Nama tabel di database
    id = db.Column(db.Integer, primary_key=True)  # ID unik untuk label
    fabric_name = db.Column(db.String(100), nullable=False)  # Nama kain
    region = db.Column(db.String(100), nullable=False)  # Wilayah asal kain
    description = db.Column(db.Text, nullable=False)  # Deskripsi label
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # Waktu pembuatan label

    def __init__(self, fabric_name, region, description):
        """Inisialisasi atribut label."""
        self.fabric_name = fabric_name 
        self.region = region
        self.description = description
