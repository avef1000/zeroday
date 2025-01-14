### routes.py ###
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mail import Message
from . import db, mail
from .models import User
from .utils import send_verification_email, verify_verification_token
from flask import Blueprint

bp = Blueprint('main', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/services')
def services():
    return render_template('services.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/testimonials')
def testimonials():
    return render_template('testimonials.html')

@bp.route('/team')
def team():
    return render_template('team.html')

@bp.route('/contact')
def contact():
    return render_template('contact.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            if user.is_verified:
                login_user(user)
                return redirect(url_for('main.employee_dashboard' if user.role == 'employee' else 'main.home'))
            else:
                flash('Please verify your email before logging in.', 'warning')
        else:
            flash('Invalid credentials. Please try again.', 'error')
    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        role = 'employee' if email.endswith('@zerodaysecurity.org') else 'customer'

        if User.query.filter_by(email=email).first():
            flash('Email already in use.', 'error')
            return redirect(url_for('main.register'))

        new_user = User(username=username, email=email, password=generate_password_hash(password), role=role)
        db.session.add(new_user)
        db.session.commit()

        send_verification_email(email)

        flash('Registration successful! Please check your email for verification.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/employee-dashboard')
@login_required
def employee_dashboard():
    if current_user.role != 'employee':
        flash('Access restricted to employees.', 'danger')
        return redirect(url_for('main.home'))
    return render_template('employee_dashboard.html')

@bp.route('/account')
@login_required
def account():
    if current_user.role == 'employee':
        return redirect(url_for('main.employee_dashboard'))
    return render_template('account.html', user=current_user)

@bp.route('/verify-email/<token>')
def verify_email(token):
    email = verify_verification_token(token)
    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.commit()
            flash('Your email has been successfully verified!', 'success')
        else:
            flash('User not found.', 'error')
    else:
        flash('Invalid or expired verification link.', 'danger')
    return redirect(url_for('main.login'))

@bp.route('/send-test-email')
def send_test_email():
    msg = Message('Test Email', recipients=['lwilliams24270@gmail.com'])
    msg.body = 'This is a test email sent from your Flask app using SpaceMail SMTP!'
    try:
        mail.send(msg)
        return 'Test email sent successfully!'
    except Exception as e:
        current_app.logger.error(f'Error sending test email: {e}')
        return 'Failed to send test email.'

@bp.route('/submit-form', methods=['POST'])
def submit_form():
    first_name = request.form.get('firstName')
    last_name = request.form.get('lastName')
    email = request.form.get('email')
    phone = request.form.get('phone')

    subject = f'New Contact Form Submission from {first_name} {last_name}'
    body = f'Name: {first_name} {last_name}\nEmail: {email}\nPhone: {phone}\n'

    try:
        msg = Message(subject=subject, sender='lwilliams@zerodaysecurity.org', recipients=['lwilliams@zerodaysecurity.org'], body=body)
        mail.send(msg)
        return jsonify({'success': True, 'message': 'Email sent successfully!'}), 200
    except Exception as e:
        current_app.logger.error(f'Error sending form email: {e}')
        return jsonify({'success': False, 'message': 'Failed to send email.'}), 500
