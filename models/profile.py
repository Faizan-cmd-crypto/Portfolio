from models import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    bio = db.Column(db.Text)
    photo = db.Column(db.String(255))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    location = db.Column(db.String(100))
    github = db.Column(db.String(255))
    linkedin = db.Column(db.String(255))
    twitter = db.Column(db.String(255))
    resume_file = db.Column(db.String(255))  # Path to the uploaded resume file
    
    def __repr__(self):
        return f'<Profile {self.name}>' 