from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize extensions
db = SQLAlchemy()  # Initialize SQLAlchemy for database
bcrypt = Bcrypt()  # Initialize Bcrypt for password hashing

class User(UserMixin, db.Model):
    __tablename__ = 'users'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique user ID
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    email = db.Column(db.String(120), unique=True, nullable=False)  # Unique user email
    password_hash = db.Column(db.String(255), nullable=False)  # Password hash
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # Registration time
    last_login_at = db.Column(db.DateTime, nullable=True)  # Last login time

    def set_password(self, password):
        """Set password and hash it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if password matches hash."""
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
    __tablename__ = 'labels'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Unique label ID
    fabric_name = db.Column(db.String(100), nullable=False)  # Fabric name
    region = db.Column(db.String(100), nullable=False)  # Fabric origin region
    description = db.Column(db.Text, nullable=False)  # Label description
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)  # Label creation time

    def __init__(self, fabric_name, region, description):
        """Initialize label attributes."""
        self.fabric_name = fabric_name
        self.region = region
        self.description = description
        
class SearchHistory(db.Model):
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    query_image = db.Column(db.String(255), nullable=False)
    search_timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship with User model to get username
    user = db.relationship('User', backref=db.backref('searches', lazy=True))
    
    def __repr__(self):
        return f'<SearchHistory {self.user.username} - {self.search_timestamp}>'

class SongketFeatures(db.Model):
    __tablename__ = 'songket_features'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    image_name = db.Column(db.String(255), nullable=False, unique=True)
    features = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return f'<SongketFeatures image_name={self.image_name}>'