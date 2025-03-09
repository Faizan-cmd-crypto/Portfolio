from flask import Blueprint, render_template, redirect, url_for, send_from_directory, current_app
from models.profile import Profile
from models.skill import Skill
from models.experience import Experience
from models.project import Project
import os

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the homepage with portfolio information."""
    # Get profile information
    profile = Profile.query.first()
    # Get skills grouped by category
    skills = Skill.query.order_by(Skill.category).all()
    # Get experiences ordered by end date (most recent first)
    experiences = Experience.query.order_by(Experience.end_date.desc()).all()
    # Get featured projects (most recent)
    projects = Project.query.order_by(Project.date.desc()).limit(3).all()
    
    return render_template('main/index.html', 
                           profile=profile,
                           skills=skills,
                           experiences=experiences,
                           projects=projects)

@main_bp.route('/about')
def about():
    """Render the about page."""
    profile = Profile.query.first()
    return render_template('main/about.html', profile=profile)

@main_bp.route('/contact')
def contact():
    """Render the contact page."""
    profile = Profile.query.first()
    return render_template('main/contact.html', profile=profile)

@main_bp.route('/resume')
def resume():
    """Render the resume page."""
    profile = Profile.query.first()
    skills = Skill.query.order_by(Skill.category).all()
    experiences = Experience.query.order_by(Experience.end_date.desc()).all()
    
    return render_template('main/resume.html', 
                           profile=profile,
                           skills=skills,
                           experiences=experiences)

@main_bp.route('/download-resume')
def download_resume():
    """Download the resume as a PDF."""
    profile = Profile.query.first()
    
    # If profile has a resume file path, use that
    if profile and profile.resume_file:
        # Assuming resume_file is stored as a path relative to the static/uploads directory
        return send_from_directory(
            os.path.join(current_app.root_path, 'static', 'uploads'),
            profile.resume_file,
            as_attachment=True,
            download_name=f"{profile.name.replace(' ', '_')}_Resume.pdf" if profile.name else "Resume.pdf"
        )
    
    # If no custom resume file, fall back to a default resume if it exists
    default_resume_path = os.path.join(current_app.root_path, 'static', 'files', 'resume.pdf')
    if os.path.exists(default_resume_path):
        return send_from_directory(
            os.path.join(current_app.root_path, 'static', 'files'),
            'resume.pdf',
            as_attachment=True,
            download_name=f"{profile.name.replace(' ', '_')}_Resume.pdf" if profile and profile.name else "Resume.pdf"
        )
    
    # If no resume is available, redirect back to the resume page
    # In a real app, you might want to show a message to the user
    return redirect(url_for('main.resume')) 