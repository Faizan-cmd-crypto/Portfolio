from models import db
from datetime import datetime

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    thumbnail = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    github_link = db.Column(db.String(255))
    live_link = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    category = db.relationship('Category', backref=db.backref('projects', lazy=True))
    
    def __repr__(self):
        return f'<Project {self.title}>'
