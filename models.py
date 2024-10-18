from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Inisialisasi ekstensi
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = 'users' 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) 
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # Waktu pendaftaran
    last_login_at = db.Column(db.DateTime, nullable=True)  # Waktu login terakhir

    def set_password(self, password):
        """Atur password dan hash-nya."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Periksa apakah password yang diberikan cocok dengan password yang di-hash."""
        return check_password_hash(self.password_hash, password)

class SongketDataset(db.Model):
    __tablename__ = 'songket_dataset'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(120), nullable=False)
    fabric_name = db.Column(db.String(120), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    uploaded_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # Waktu unggah data

    def __init__(self, region, fabric_name, image_filename):
        self.region = region
        self.fabric_name = fabric_name
        self.image_filename = image_filename

class Label(db.Model):
    __tablename__ = 'labels' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False) 
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    def __init__(self, name, region, description):
        self.name = name
        self.region = region
        self.description = description
