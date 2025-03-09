from models import db
from datetime import datetime

class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100))
    location = db.Column(db.String(100))
    type = db.Column(db.String(20))  # "work", "education", etc.
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Experience {self.title} at {self.company}>' 