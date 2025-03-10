import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models import db
from authlib.integrations.flask_client import OAuth

auth_bp = Blueprint('auth', __name__)

# Setup OAuth
oauth = OAuth()

@auth_bp.record_once
def on_load(state):
    app = state.app
    oauth.init_app(app)
    
    # Configure OAuth providers
    oauth.register(
        name='github',
        client_id=os.getenv('GITHUB_CLIENT_ID'),
        client_secret=os.getenv('GITHUB_CLIENT_SECRET'),
        authorize_url='https://github.com/login/oauth/authorize',
        authorize_params=None,
        access_token_url='https://github.com/login/oauth/access_token',
        access_token_params=None,
        refresh_token_url=None,
        client_kwargs={'scope': 'user:email'},
    )

@auth_bp.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('admin.index'))
        flash('Invalid credentials')
    return render_template('auth/login.html')

@auth_bp.route('/auth/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth_bp.route('/auth/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        if not check_password_hash(current_user.password, current_password):
            flash('Current password is incorrect')
            return redirect(url_for('auth.change_password'))
            
        if new_password != confirm_password:
            flash('New passwords do not match')
            return redirect(url_for('auth.change_password'))
            
        current_user.password = generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully')
        return redirect(url_for('admin.index'))
        
    return render_template('auth/change_password.html')

@auth_bp.route('/login/github')
def github_login():
    """Initiate GitHub OAuth login."""
    redirect_uri = url_for('auth.github_authorize', _external=True)
    return oauth.github.authorize_redirect(redirect_uri)

@auth_bp.route('/login/github/callback')
def github_authorize():
    """Handle GitHub OAuth callback."""
    token = oauth.github.authorize_access_token()
    resp = oauth.github.get('https://api.github.com/user', token=token)
    profile = resp.json()
    
    # Check if user exists, create if not
    user = User.query.filter_by(email=profile.get('email')).first()
    
    if not user:
        user = User(
            email=profile.get('email'),
            name=profile.get('name'),
            password=generate_password_hash('github-oauth-user', method='pbkdf2:sha256'),
            oauth_provider='github',
            oauth_id=str(profile.get('id'))
        )
        db.session.add(user)
        db.session.commit()
    
    login_user(user)
    return redirect(url_for('main.index')) 