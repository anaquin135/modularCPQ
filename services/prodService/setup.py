from app import db, bcrypt
from app.models import *
import json
import datetime 
import pandas

db.drop_all()
db.create_all()

csModel = MODEL()
csModel.varName = 'cs_staff'
csModel.label   = "Staff"
csModel.family  = "Cloud Services"
csModel.attrSet = 1
db.session.add(csModel)

attr = ATTRSET()
attr.attr1Label = "Location"
attr.attr2Label = "Category"
attr.attr3Label = "Skill"
attr.attr4Label = "null"
attr.attr5Label = "null"
attr.attr1LOV   = "null#Onshore#Offshore"
attr.attr2LOV   = "null#Functional#Technical"
attr.attr3LOV   = "null#Senior#Junior#Intern"
attr.attr4LOV   = "null"
attr.attr5LOV   = "null"
db.session.add(attr)

# PARTS #
pfile = pandas.read_csv('parts.csv')
pdict = pfile.to_dict(orient='records')
for part in pdict:
    newPart = PRODUCT()
    newPart.partNum      = part['partNum']
    newPart.description  = part['description']
    newPart.isActive     = part['isActive']
    newPart.listNRC      = part['listNRC']
    newPart.listMRC      = part['listMRC']
    newPart.productModel = part['productModel']
    newPart.attrVal1     = part['attrVal1']
    newPart.attrVal2     = part['attrVal2']
    newPart.attrVal3     = part['attrVal3']
    newPart.attrVal4     = part['attrVal4']
    newPart.attrVal5     = part['attrVal5']
    db.session.add(newPart)

db.session.commit()