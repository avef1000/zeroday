
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
    # Query all users in the database and delete them
    all_users = User.query.all()
    for user in all_users:
        db.session.delete(user)

    # Commit the transaction to delete the users from the database
    db.session.commit()

    print(f"Successfully deleted {len(all_users)} user(s) from the database.")
