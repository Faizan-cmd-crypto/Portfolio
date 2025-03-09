from app import app, db
from models import User, Profile, Category, Skill, Project, Experience
from werkzeug.security import generate_password_hash
import os

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if admin user exists
        if not User.query.filter_by(email='faizanahmad1127@gmail.com').first():
            # Create admin user
            admin = User(
                email='faizanahmad1127@gmail.com',
                password=generate_password_hash('admin6194214054'),
                is_admin=True
            )
            db.session.add(admin)
            
            # Create initial profile
            profile = Profile(
                full_name='Faizan Ahmad',
                title='Full Stack Developer',
                description='Passionate about creating innovative web solutions',
                location='Pakistan',
                email='faizanahmad1127@gmail.com',
                phone='+92 3164214054',
                github='https://github.com/yourusername',
                linkedin='https://linkedin.com/in/yourusername'
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

if __name__ == '__main__':
    init_db() 