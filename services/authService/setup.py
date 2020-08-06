from app import db, bcrypt
from app.models import USER

db.drop_all()
db.create_all()

sampleUser = USER()
sampleUser.firstName = "Bob"
sampleUser.lastName = "Dylan"
sampleUser.jobTitle = "CIO"
sampleUser.email = "admin@email.com"
sampleUser.password = bcrypt.generate_password_hash('wasspord')
sampleUser.isActive = True
sampleUser.accessLevel = 2
sampleUser.isPwdExp = False

db.session.add(sampleUser)
db.session.commit()
