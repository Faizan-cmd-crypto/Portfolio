from app import create_app
from models import db
from models.user import User
from models.profile import Profile
from models.project import Project
from models.category import Category
from models.skill import Skill
from models.experience import Experience
from werkzeug.security import generate_password_hash
import sys

def init_db():
    """Reset the database and initialize it with sample data."""
    print("WARNING: This will delete all existing data in the database!")
    print("Type 'yes' to continue or anything else to cancel...")
    
    confirmation = input().lower()
    if confirmation != 'yes':
        print("Operation cancelled.")
        sys.exit(0)
    
    app = create_app()
    with app.app_context():
        # Drop and recreate all tables
        print("Dropping all tables...")
        db.drop_all()
        print("Creating new tables...")
        db.create_all()
        
        print("Creating sample data...")
        # Create admin user
        admin = User(
            email='faizanahmad1127@gmail.com',
            password=generate_password_hash('admin6194214054', method='pbkdf2:sha256'),
            name='Admin User',
            is_admin=True
        )
        db.session.add(admin)
        
        # Create sample profile
        profile = Profile(
            name='Faizan Ahmad',
            title='Full Stack Developer',
            bio='Passionate developer with expertise in web development and a knack for creating beautiful, functional applications.',
            email='faizanahmad1127@gmail.com',
            location='Srinagar, jammu and Kashmir',
            github='https://github.com/Faizan-cmd-crypto',
            linkedin='https://linkedin.com/in/Faizan_Ahmad'
        )
        db.session.add(profile)
        
        # Create sample categories
        categories = [
            Category(name='Web Development'),
            Category(name='Mobile Apps'),
            Category(name='UI/UX Design'),
            Category(name='Machine Learning')
        ]
        db.session.add_all(categories)
        
        # Create sample skills
        skills = [
            Skill(name='Python', level=90, category='Backend'),
            Skill(name='JavaScript', level=85, category='Frontend'),
            Skill(name='React', level=80, category='Frontend'),
            Skill(name='Flask', level=85, category='Backend'),
            Skill(name='MongoDB', level=75, category='Database'),
            Skill(name='Tailwind CSS', level=90, category='Frontend'),
            Skill(name='Next.js', level=70, category='Frontend and Backend'),
            Skill(name='Git', level=85, category='DevOps')
        ]
        db.session.add_all(skills)
        
        # Commit to save the initial data
        db.session.commit()
        print("Database initialized successfully with sample data!")
        print("\nIMPORTANT: Do not run this script again unless you want to delete all your data!")

if __name__ == '__main__':
    init_db() 