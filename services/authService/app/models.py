from datetime import datetime
from app import db

class USER(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    createdDate = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    firstName = db.Column(db.String(120), nullable=False)
    lastName = db.Column(db.String(120), nullable=False)
    jobTitle = db.Column(db.String(120), nullable=False, default='Sales')
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    isActive = db.Column(db.Boolean, nullable=False, default=True)
    manager = db.Column(db.Integer, nullable=True)
    accessLevel = db.Column(db.Integer, nullable=False, default=1) #1 - Sales, #2 - Business Admin
    deactivateDate = db.Column(db.DateTime, nullable=True)
    photo = db.Column(db.String(300), nullable=False, default='default.jpg')
    businessLine = db.Column(db.String(120), nullable=False, default='Cloud Services')
    isPwdExp = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f'''
                id: '{self.id}', 
                Is Active: '{self.isActive}',
                Name: '{self.firstName}' '{self.lastName}',
                Email: '{self.email}',
                Job Title: '{self.jobTitle}',
                Access Level: '{self.accessLevel}',
                Manager ID: '{self.manager}',
                Business Line: '{self.businessLine}'
                '''