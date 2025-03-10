import os
from flask import Flask, render_template
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from dotenv import load_dotenv
from models import db, init_db
from models.user import User
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize extensions
migrate = Migrate()
login_manager = LoginManager()
ckeditor = CKEditor()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-development')
    # Configure database
    database_url = os.getenv('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///portfolio.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    init_db(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    
    login_manager.login_view = 'auth.login'
    
    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.projects import projects_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(projects_bp, url_prefix='/projects')
    
    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error/500.html'), 500
    
    # Add template context processors
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}
    
    return app

# Create the app instance
app = create_app()

# Ensure we have an application context
with app.app_context():
    # Initialize database (only create tables if they don't exist)
    db.create_all()
    
    # Check if there are any users (if not, it's a new database and we need sample data)
    if User.query.count() == 0:
        # Import the initialization function to create sample data
        from init_db import create_sample_data
        create_sample_data()

if __name__ == '__main__':
    app.run(debug=True)