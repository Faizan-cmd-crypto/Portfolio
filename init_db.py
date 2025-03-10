from app import app, db
from models import User, Profile, Category, Skill, Project, Experience
from werkzeug.security import generate_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

def init_db():
    """Reset the database and initialize it with sample data."""
    print("WARNING: This will delete all existing data in the database!")
    print("Type 'yes' to continue or anything else to cancel...")
    
    confirmation = input().lower()
    if confirmation != 'yes':
        print("Operation cancelled.")
        return
    
    with app.app_context():
        # Drop and recreate all tables
        print("Dropping all tables...")
        db.drop_all()
        print("Creating new tables...")
        db.create_all()
        
        print("Creating sample data...")
        # Check if admin user exists
        admin_email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
        if not User.query.filter_by(email=admin_email).first():
            # Create admin user
            admin = User(
                email=admin_email,
                password=generate_password_hash(os.getenv('ADMIN_PASSWORD', 'changeme')),
                is_admin=True
            )
            db.session.add(admin)
            
            # Create initial profile
            profile = Profile(
                full_name=os.getenv('ADMIN_NAME', 'Admin User'),
                title='Full Stack Developer',
                description='Passionate about creating innovative web solutions',
                location='Your Location',
                email=admin_email,
                phone=os.getenv('ADMIN_PHONE', ''),
                github=os.getenv('GITHUB_URL', ''),
                linkedin=os.getenv('LINKEDIN_URL', '')
            )
            db.session.add(profile)
            
            # Create some initial categories
            categories = [
                Category(name='Frontend Development'),
                Category(name='Backend Development'),
                Category(name='Database'),
                Category(name='DevOps')
            ]
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            print("Database initialized with admin user and initial data!")
        else:
            print("Admin user already exists!")
        print("\nIMPORTANT: Do not run this script again unless you want to delete all your data!")

if __name__ == '__main__':
    init_db() 