from datetime import datetime
from app import db

class DOCUMENT(db.Model):
        id           = db.Column(db.Integer, nullable=False, primary_key=True)
        description  = db.Column(db.String(300), nullable=False, default='Missing Description')
        isActive     = db.Column(db.Boolean, nullable=False, default=True)
        template     = db.Column(db.String(300), nullable=False)

class TERMS(db.Model):
        id           = db.Column(db.Integer, nullable=False, primary_key=True)
        description  = db.Column(db.String(300), nullable=False, default='Missing Description')
        isActive     = db.Column(db.Boolean, nullable=False, default=True)
        template     = db.Column(db.String(300), nullable=False)
        enabledPNs   = db.Column(db.Text, nullable=False, default='ALL')
