# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# Initialize extensions
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
migrate = Migrate()

# Load environment variables from .env
load_dotenv()

def create_app():
    # Initialize the Flask app
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24))  # Use env or generate
    app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT', os.urandom(16))  # Use env or generate
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance', 'users.db')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Email configuration
    app.config['MAIL_SERVER'] = 'mail.spacemail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = 'lwilliams@zerodaysecurity.org'
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')  # Load from .env
    app.config['MAIL_DEFAULT_SENDER'] = 'lwilliams@zerodaysecurity.org'

    # Add BASE_URL to the configuration
    app.config['BASE_URL'] = os.getenv('BASE_URL', 'http://localhost:5000')  # Add your actual base URL here

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "routes.login"  # Adjust this if your login view is different

    # Define user_loader for flask-login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import routes and register blueprints
    from .routes import bp  # Import after app setup
    app.register_blueprint(bp)

    # Ensure the directory for the database file exists
    db_dir = os.path.join(os.path.dirname(__file__), 'instance')
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Create the database tables
    with app.app_context():
        db.create_all()

    return app
