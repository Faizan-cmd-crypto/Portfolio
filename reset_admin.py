from app import app, db
from models.user import User
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

def reset_admin():
    with app.app_context():
        # Try to find the admin user
        admin_email = os.getenv('ADMIN_EMAIL', 'faizanahmad1127@gmail.com')
        admin = User.query.filter_by(email=admin_email).first()
        
        if admin:
            # Reset existing admin's password
            admin.password = generate_password_hash('Faizan6194214054')
            db.session.commit()
            print(f"Admin password has been reset!")
        else:
            # Create new admin user
            new_admin = User(
                email=admin_email,
                password=generate_password_hash('Faizan6194214054'),
                is_admin=True
            )
            db.session.add(new_admin)
            db.session.commit()
            print(f"New admin user has been created!")
        
        print("\nYou can now login with:")
        print(f"Email: {admin_email}")
        print("Password: Faizan6194214054")

if __name__ == '__main__':
    reset_admin() 