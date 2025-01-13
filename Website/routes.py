from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from flask_mail import Message
from werkzeug.security import check_password_hash, generate_password_hash
from . import db, mail  # Import db and mail from the app factory
from .models import User  # Import the User model here to avoid circular import issues
from .utils import send_verification_email, verify_verification_token  # Import utils functions

from flask import Blueprint, request, flash, redirect, url_for
from flask_mail import Message
from Website import mail
from flask import jsonify


bp = Blueprint('main', __name__)

# Home route
@bp.route("/")
def home():
    return render_template("index.html")

# Services route
@bp.route("/services")
def services():
    return render_template("services.html")

# About route
@bp.route("/about")
def about():
    return render_template("about.html")

# Testimonials route
@bp.route("/testimonials")
def testimonials():
    return render_template("testimonials.html")

# Team route
@bp.route("/team")
def team():
    return render_template("team.html")

# Contact route
@bp.route("/contact")
def contact():
    return render_template("contact.html")

# Login route
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            if user.is_verified:  # Ensure email is verified
                login_user(user)
                # Redirect based on role
                if user.role == 'employee':
                    return redirect(url_for("main.employee_dashboard"))
                else:
                    return redirect(url_for("main.home"))
            else:
                flash("Please verify your email before logging in.", "warning")
        else:
            flash("Invalid credentials. Please try again.", "error")
    
    return render_template("login.html")

# Logout route
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("main.home"))

# Register route
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if email is for an employee
        role = 'employee' if email.endswith('@zerodaysecurity.org') else 'customer'

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already in use.", 'error')
            return redirect(url_for('main.register'))

        # Create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()

        # Send verification email
        send_verification_email(email)

        flash("Registration successful! A verification email has been sent. Please check your inbox.", 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

# Employee dashboard route
@bp.route("/employee-dashboard")
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash("Access restricted to employees.", "danger")
        return redirect(url_for("main.home"))
    
    return render_template("employee_dashboard.html")

# Account route for logged-in users
@bp.route("/account")
@login_required
def account():
    if current_user.role == 'employee':
        return redirect(url_for("main.employee_dashboard"))
    return render_template("account.html", user=current_user)

# Verification email route
@bp.route('/verify-email/<token>')
def verify_email(token):
    email = verify_verification_token(token)
    if email is None:
        flash("The verification link is invalid or has expired.", 'danger')
        return redirect(url_for('main.login'))

    # Mark the user's email as verified in the database
    user = User.query.filter_by(email=email).first()
    if user:
        user.is_verified = True
        db.session.commit()
        flash("Your email has been successfully verified!", 'success')
    else:
        flash("User not found.", 'error')

    return redirect(url_for('main.login'))

# Test email route (for debugging)
@bp.route('/send-test-email')
def send_test_email():
    msg = Message("Test Email", recipients=["lwilliams24270@gmail.com"])
    msg.body = "This is a test email sent from your Flask app using SpaceMail SMTP!"
    
    try:
        mail.send(msg)
        return "Test email sent successfully!"
    except Exception as e:
        print(f"Error: {e}")
        return "Failed to send test email."

@bp.route('/submit-form', methods=['POST'])
def submit_form():
    # Get form data
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phone')

    # Compose email content
    subject = f"New Contact Form Submission from {first_name} {last_name}"
    body = (
        f"Name: {first_name} {last_name}\n"
        f"Email: {email}\n"
        f"Phone: {phone}\n"
    )

    # Send email
    try:
        msg = Message(
            subject=subject,
            sender='lwilliams@zerodaysecurity.org',
            recipients=['lwilliams@zerodaysecurity.org'],
            body=body
        )
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Email sent successfully!'}), 200
    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'success': False, 'message': 'Failed to send email.'}), 500
