from datetime import datetime
from app import db

class OPP(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    customerName  = db.Column(db.String(120), nullable=False)
    desc          = db.Column(db.String(500), nullable=True)
    contractTerm  = db.Column(db.Integer, nullable=False)
    requestOwner  = db.Column(db.Integer, nullable=False)
    #requestTeam   = db.Column(db.String(50), nullable=True)
    requestStatus = db.Column(db.String(50), nullable=False, default='In Progress')
    createdDate   = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lastModified  = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tcv           = db.Column(db.Float, nullable=False, default=0.0)
    bundle        = db.Column(db.JSON, nullable=True)
    
    ''' BUNDLE KEYS
            'partNumber'
            'description'
            'qtyNew'
            'qtyExi'
            'listNRC'
            'listMRC'
            'discNRC'
            'discMRC'
            'netNRC'
            'netMRC'
            vvv NEW ITEMS
            'extNRC'
            'extMRC'
    '''

    def __repr__(self):
        return f'''
                id: '{self.id}', 
                Customer Name: '{self.customerName}',
                Description: '{self.desc}',
                Contract Term: '{self.contractTerm}',
                Request Owner: '{self.requestOwner}',
                Request Status: '{self.requestStatus}'
                '''