from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False) 

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    
class SongketDataset(db.Model):
    __tablename__ = 'songket_dataset'
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(120), nullable=False)
    fabric_name = db.Column(db.String(120), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)

    def __init__(self, region, fabric_name, image_filename):
        self.region = region
        self.fabric_name = fabric_name
        self.image_filename = image_filename
