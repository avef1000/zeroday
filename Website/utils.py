from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from . import mail
from flask import current_app

# Email verification utility functions
def send_verification_email(user_email):
    token = generate_verification_token(user_email)
    verification_url = f"{current_app.config['BASE_URL']}/verify-email/{token}"
    msg = Message("Email Verification", recipients=[user_email])
    msg.body = f"Please click the following link to verify your email: {verification_url}"

    try:
        mail.send(msg)
    except Exception as e:
        print(f"Error sending verification email: {e}")

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_verification_token(token, expiration=3600):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
        return email
    except Exception as e:
        print(f"Error verifying token: {e}")
        return None
