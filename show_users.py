# show_users.py

import sys
import os
from Website import create_app, db
from Website.models import User

# Add the 'Website' directory to sys.path so it can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Website')))

# Create an app instance
app = create_app()

# Ensure the app context is pushed so database operations can be performed
with app.app_context():
    # Query all users in the database
    employees = User.query.filter_by(role='employee').all()
    customers = User.query.filter_by(role='customer').all()

    # Print employees and customers
    print("Employees:")
    for employee in employees:
        print(f"ID: {employee.id}, Username: {employee.username}, Email: {employee.email}")

    print("\nCustomers:")
    for customer in customers:
        print(f"ID: {customer.id}, Username: {customer.username}, Email: {customer.email}")
