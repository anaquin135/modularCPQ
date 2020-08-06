from app import db, bcrypt
from app.models import OPP
import json
import datetime 

db.drop_all()
db.create_all()

sampleOPP = OPP()
sampleOPP.customerName = "Hitgub"
sampleOPP.desc          = "This is a sample deal."
sampleOPP.contractTerm  = "36"

tod = datetime.datetime.now()
d = datetime.timedelta(days = 50)
a = tod - d
sampleOPP.createdDate  = a
sampleOPP.lastModified = a

sampleOPP.requestOwner  = 1

#INV
CI = {
        'partNumber':'CSNF01',
        'description':'Project Manager',
        'qtyNew':1,
        'qtyExi':0,
        'listNRC':0.00,
        'listMRC':12500.00,
        'discNRC':0.00,
        'discMRC':0.00,
        'netNRC':0.00,
        'netMRC':12500.00,
        'extNRC':0.00,
        'extMRC':12500.00
}
CI2 = {
        'partNumber':'CSNF02',
        'description':'Senior Functional Consultant',
        'qtyNew':2,
        'qtyExi':0,
        'listNRC':0.00,
        'listMRC':5000.00,
        'discNRC':0.00,
        'discMRC':0.00,
        'netNRC':0.00,
        'netMRC':5000.00,
        'extNRC':0.00,
        'extMRC':10000.00
}
parent = {
        "0":CI,
        "1":CI2,
        "2":CI2,
        "3":CI2,
        "4":CI2,
        "5":CI2
}
invJson = json.dumps(parent)
sampleOPP.bundle = invJson


db.session.add(sampleOPP)
db.session.commit()