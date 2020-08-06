from datetime import datetime
from app import db

class PRODUCT(db.Model):
        partNum      = db.Column(db.String(120), nullable=False, primary_key=True)
        description  = db.Column(db.String(300), nullable=False, default='Missing Description')
        isActive     = db.Column(db.Boolean, nullable=False, default=True)
        listNRC      = db.Column(db.Float, nullable=False, default=0.0)
        listMRC      = db.Column(db.Float, nullable=False, default=0.0)
        productModel = db.Column(db.String(120), nullable=False) #Unconstrained foreign key
        attrVal1     = db.Column(db.Integer, nullable=False, default=0)
        attrVal2     = db.Column(db.Integer, nullable=False, default=0)
        attrVal3     = db.Column(db.Integer, nullable=False, default=0)
        attrVal4     = db.Column(db.Integer, nullable=False, default=0)
        attrVal5     = db.Column(db.Integer, nullable=False, default=0)

class MODEL(db.Model):
        varName  = db.Column(db.String(120), nullable=False, primary_key=True)
        label    = db.Column(db.String(300), nullable=False)
        family   = db.Column(db.String(300), nullable=False)
        attrSet  = db.Column(db.Integer, nullable=False) #Unconstrained foreign key
        isActive = db.Column(db.Boolean, nullable=False, default=True)
        configType = db.Column(db.String(120), nullable=False, default='simple')

class ATTRSET(db.Model):
        id         = db.Column(db.Integer, nullable=False, primary_key=True)
        attr1Label = db.Column(db.String(300), nullable=False)
        attr2Label = db.Column(db.String(300), nullable=False)
        attr3Label = db.Column(db.String(300), nullable=False)
        attr4Label = db.Column(db.String(300), nullable=False)
        attr5Label = db.Column(db.String(300), nullable=False)

        attr1LOV = db.Column(db.Text, nullable=False)
        attr2LOV = db.Column(db.Text, nullable=False)
        attr3LOV = db.Column(db.Text, nullable=False)
        attr4LOV = db.Column(db.Text, nullable=False)
        attr5LOV = db.Column(db.Text, nullable=False)
