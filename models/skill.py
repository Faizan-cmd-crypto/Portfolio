from models import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer)  # 1-100 percentage
    category = db.Column(db.String(50))  # e.g., "Frontend", "Backend", "Database", etc.
    
    def __repr__(self):
        return f'<Skill {self.name}>' 