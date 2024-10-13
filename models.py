from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

# Model untuk dataset songket
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
