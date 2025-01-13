import os

# Generate SECRET_KEY (24 bytes random value)
secret_key = os.urandom(24)
print(f"SECRET_KEY={secret_key.hex()}")

# Generate SECURITY_PASSWORD_SALT (16 bytes random value)
password_salt = os.urandom(16)
print(f"SECURITY_PASSWORD_SALT={password_salt.hex()}")
