from flask import Blueprint, render_template, request, jsonify, abort
from models.project import Project
from models.category import Category

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/')
def index():
    """Display all projects with optional filtering."""
    category_id = request.args.get('category', type=int)
    
    # Get all categories for the filter
    categories = Category.query.all()
    
    # Filter projects by category if specified
    if category_id:
        projects = Project.query.filter_by(category_id=category_id).order_by(Project.date.desc()).all()
    else:
        projects = Project.query.order_by(Project.date.desc()).all()
    
    return render_template('projects/index.html', 
                          projects=projects,
                          categories=categories,
                          selected_category=category_id)

@projects_bp.route('/<int:project_id>')
def show(project_id):
    """Display a single project with detailed information."""
    project = Project.query.get_or_404(project_id)
    
    # Get related projects (same category, excluding current)
    related_projects = Project.query.filter(
        Project.category_id == project.category_id,
        Project.id != project.id
    ).limit(3).all()
    
    return render_template('projects/show.html', 
                          project=project,
                          related_projects=related_projects)

@projects_bp.route('/api/list')
def api_list():
    """JSON API endpoint for projects (useful for AJAX filtering)."""
    category_id = request.args.get('category', type=int)
    
    if category_id:
        projects = Project.query.filter_by(category_id=category_id).order_by(Project.date.desc()).all()
    else:
        projects = Project.query.order_by(Project.date.desc()).all()
    
    result = [{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'thumbnail': p.thumbnail,
        'category': p.category.name if p.category else None,
        'date': p.date.strftime('%B %Y') if p.date else None
    } for p in projects]
    
    return jsonify(result) 