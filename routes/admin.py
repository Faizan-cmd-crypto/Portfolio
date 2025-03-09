from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models.profile import Profile
from models.project import Project
from models.category import Category
from models.skill import Skill
from models.experience import Experience
from models import db
from flask_ckeditor import upload_success, upload_fail
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

# Middleware to check if user is admin
@admin_bp.before_request
def check_admin():
    if not current_user.is_authenticated or not current_user.is_admin:
        flash('You do not have permission to access the admin area.', 'danger')
        return redirect(url_for('main.index'))

@admin_bp.route('/')
@login_required
def index():
    """Admin dashboard."""
    project_count = Project.query.count()
    category_count = Category.query.count()
    skill_count = Skill.query.count()
    experience_count = Experience.query.count()
    
    return render_template('admin/index.html',
                          project_count=project_count,
                          category_count=category_count,
                          skill_count=skill_count,
                          experience_count=experience_count)

# Profile management
@admin_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """Edit personal profile information."""
    profile = Profile.query.first()
    if not profile:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()
    
    if request.method == 'POST':
        profile.name = request.form.get('name')
        profile.title = request.form.get('title')
        profile.bio = request.form.get('bio')
        profile.email = request.form.get('email')
        profile.phone = request.form.get('phone')
        profile.location = request.form.get('location')
        profile.github = request.form.get('github')
        profile.linkedin = request.form.get('linkedin')
        profile.twitter = request.form.get('twitter')
        
        # Handle profile photo upload
        if 'photo' in request.files and request.files['photo'].filename:
            file = request.files['photo']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images/uploads', filename)
            file.save(file_path)
            profile.photo = f'/static/images/uploads/{filename}'
        
        # Handle resume file upload
        if 'resume_file' in request.files and request.files['resume_file'].filename:
            file = request.files['resume_file']
            if file.filename.lower().endswith('.pdf'):
                filename = secure_filename(file.filename)
                # Ensure the uploads directory exists
                os.makedirs(os.path.join(current_app.root_path, 'static/uploads'), exist_ok=True)
                file_path = os.path.join(current_app.root_path, 'static/uploads', filename)
                file.save(file_path)
                profile.resume_file = filename
            else:
                flash('Resume must be a PDF file', 'danger')
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('admin.profile'))
    
    return render_template('admin/profile.html', profile=profile)

# Project management
@admin_bp.route('/projects')
@login_required
def projects():
    """List all projects."""
    projects = Project.query.order_by(Project.date.desc()).all()
    return render_template('admin/projects/index.html', projects=projects)

@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
def new_project():
    """Create a new project."""
    categories = Category.query.all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content = request.form.get('content')
        category_id = request.form.get('category_id', type=int)
        date_str = request.form.get('date')
        github_link = request.form.get('github_link')
        live_link = request.form.get('live_link')
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else None
        except ValueError:
            date = None
        
        project = Project(
            title=title,
            description=description,
            content=content,
            category_id=category_id,
            date=date,
            github_link=github_link,
            live_link=live_link
        )
        
        # Handle thumbnail upload
        if 'thumbnail' in request.files and request.files['thumbnail'].filename:
            file = request.files['thumbnail']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images/projects', filename)
            file.save(file_path)
            project.thumbnail = f'/static/images/projects/{filename}'
        
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/projects/form.html', project=None, categories=categories)

@admin_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    """Edit an existing project."""
    project = Project.query.get_or_404(project_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        project.title = request.form.get('title')
        project.description = request.form.get('description')
        project.content = request.form.get('content')
        project.category_id = request.form.get('category_id', type=int)
        project.github_link = request.form.get('github_link')
        project.live_link = request.form.get('live_link')
        date_str = request.form.get('date')
        
        try:
            project.date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None
        except ValueError:
            pass
        
        # Handle thumbnail upload if provided
        if 'thumbnail' in request.files and request.files['thumbnail'].filename:
            file = request.files['thumbnail']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images/projects', filename)
            file.save(file_path)
            project.thumbnail = f'/static/images/projects/{filename}'
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin.projects'))
    
    return render_template('admin/projects/form.html', project=project, categories=categories)

@admin_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    """Delete a project."""
    project = Project.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin.projects'))

# Category management
@admin_bp.route('/categories')
@login_required
def categories():
    """List all categories."""
    categories = Category.query.all()
    return render_template('admin/categories/index.html', categories=categories)

@admin_bp.route('/categories/new', methods=['GET', 'POST'])
@login_required
def new_category():
    """Create a new category."""
    if request.method == 'POST':
        name = request.form.get('name')
        
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/categories/form.html', category=None)

@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """Edit an existing category."""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        db.session.commit()
        
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/categories/form.html', category=category)

@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    """Delete a category."""
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin.categories'))

# Skills management
@admin_bp.route('/skills')
@login_required
def skills():
    """List all skills."""
    skills = Skill.query.all()
    return render_template('admin/skills/index.html', skills=skills)

@admin_bp.route('/skills/new', methods=['GET', 'POST'])
@login_required
def new_skill():
    """Create a new skill."""
    if request.method == 'POST':
        name = request.form.get('name')
        level = request.form.get('proficiency', type=int)  # Get from proficiency field but use as level
        category = request.form.get('category')
        
        skill = Skill(
            name=name,
            level=level,  # Use level instead of proficiency
            category=category
        )
        
        # Handle icon upload if provided
        if 'icon' in request.files and request.files['icon'].filename:
            file = request.files['icon']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images/skills', filename)
            file.save(file_path)
            skill.icon = f'/static/images/skills/{filename}'
        
        db.session.add(skill)
        db.session.commit()
        
        flash('Skill created successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skills/form.html', skill=None)

@admin_bp.route('/skills/<int:skill_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    """Edit an existing skill."""
    skill = Skill.query.get_or_404(skill_id)
    
    if request.method == 'POST':
        skill.name = request.form.get('name')
        skill.level = request.form.get('proficiency', type=int)  # Get from proficiency field but use as level
        skill.category = request.form.get('category')
        
        # Handle icon upload if provided
        if 'icon' in request.files and request.files['icon'].filename:
            file = request.files['icon']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images/skills', filename)
            file.save(file_path)
            skill.icon = f'/static/images/skills/{filename}'
        
        db.session.commit()
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skills/form.html', skill=skill)

@admin_bp.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    """Delete a skill."""
    skill = Skill.query.get_or_404(skill_id)
    db.session.delete(skill)
    db.session.commit()
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('admin.skills'))

# Experience management
@admin_bp.route('/experiences')
@login_required
def experiences():
    """List all experiences."""
    experiences = Experience.query.order_by(Experience.start_date.desc()).all()
    return render_template('admin/experiences/index.html', experiences=experiences)

@admin_bp.route('/experiences/new', methods=['GET', 'POST'])
@login_required
def new_experience():
    """Create a new experience."""
    if request.method == 'POST':
        title = request.form.get('title')
        company = request.form.get('company')
        location = request.form.get('location')
        description = request.form.get('description')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        current = bool(request.form.get('current'))
        
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str and not current else None
        except ValueError:
            start_date = None
            end_date = None
        
        experience = Experience(
            title=title,
            company=company,
            location=location,
            description=description,
            start_date=start_date,
            end_date=end_date,
            current=current
        )
        
        # Handle company logo upload if provided
        if 'company_logo' in request.files and request.files['company_logo'].filename:
            file = request.files['company_logo']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images/companies', filename)
            file.save(file_path)
            experience.company_logo = f'/static/images/companies/{filename}'
        
        db.session.add(experience)
        db.session.commit()
        flash('Experience added successfully!', 'success')
        return redirect(url_for('admin.experiences'))
    
    return render_template('admin/experiences/form.html', experience=None)

@admin_bp.route('/experiences/<int:experience_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_experience(experience_id):
    """Edit an existing experience."""
    experience = Experience.query.get_or_404(experience_id)
    
    if request.method == 'POST':
        experience.title = request.form.get('title')
        experience.company = request.form.get('company')
        experience.location = request.form.get('location')
        experience.description = request.form.get('description')
        start_date_str = request.form.get('start_date')
        end_date_str = request.form.get('end_date')
        experience.current = bool(request.form.get('current'))
        
        try:
            experience.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            experience.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str and not experience.current else None
        except ValueError:
            pass
        
        # Handle company logo upload if provided
        if 'company_logo' in request.files and request.files['company_logo'].filename:
            file = request.files['company_logo']
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.root_path, 'static/images/companies', filename)
            file.save(file_path)
            experience.company_logo = f'/static/images/companies/{filename}'
        
        db.session.commit()
        flash('Experience updated successfully!', 'success')
        return redirect(url_for('admin.experiences'))
    
    return render_template('admin/experiences/form.html', experience=experience)

@admin_bp.route('/experiences/<int:experience_id>/delete', methods=['POST'])
@login_required
def delete_experience(experience_id):
    """Delete an experience."""
    experience = Experience.query.get_or_404(experience_id)
    db.session.delete(experience)
    db.session.commit()
    flash('Experience deleted successfully!', 'success')
    return redirect(url_for('admin.experiences'))

# Rich text editor file upload endpoint
@admin_bp.route('/upload', methods=['POST'])
@login_required
def upload():
    """Handle file uploads from CKEditor."""
    f = request.files.get('upload')
    if not f:
        return upload_fail('No file found')
    
    filename = secure_filename(f.filename)
    file_path = os.path.join(current_app.root_path, 'static/images/uploads', filename)
    f.save(file_path)
    url = url_for('static', filename=f'images/uploads/{filename}')
    
    return upload_success(url=url) 