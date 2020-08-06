from app import db, bcrypt
from app.models import *
import json
import datetime 

db.drop_all()
db.create_all()

doc1 = DOCUMENT()
doc1.description = "Standard quote template."
doc1.template = "doc1.html"
db.session.add(doc1)

term1 = TERMS()
term1.description = "Simple T&C for all."
term1.enabledPNs = "ALL"
term1.template = "app/static/terms/term1.html"
db.session.add(term1)

term2 = TERMS()
term2.description = "Simple T&C for all."
term2.enabledPNs = "ALL"
term2.template = "app/static/terms/term2.html"
db.session.add(term2)

term3 = TERMS()
term3.description = "Intern Clause"
term3.enabledPNs = "CSNF04#CSNT04"
term3.template = "app/static/terms/intern.html"
db.session.add(term3)

db.session.commit()