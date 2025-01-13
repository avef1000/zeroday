from . import db  # Import db from __init__.py to avoid circular imports
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # Import UserMixin from flask_login

class User(UserMixin, db.Model):  # Inherit from UserMixin to get default methods like is_active
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='customer')
    is_verified = db.Column(db.Boolean, default=False)  # Track email verification status
    is_active = db.Column(db.Boolean, default=True)  # Add this line to track user activity

    def __repr__(self):
        return f'<User {self.username}>'

    # Hash password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # Verify password
    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Email verification handler
    def verify_email(self):
        self.is_verified = True
