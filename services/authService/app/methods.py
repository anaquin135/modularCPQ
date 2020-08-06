from app import db, bcrypt
from flask import jsonify, abort, redirect, url_for, make_response
from app.models import USER
import json
import jsonpickle
from json import JSONEncoder
from datetime import datetime

# Provide Generic Success #
###########################
def provideGenericSuccess():
    return jsonify({'response': 'success'})

# Get all users #
#################
def getAllUsers():
    users = USER.query.all()
    uJSON = jsonpickle.encode(users, unpicklable=False) 
    userJSONData = json.dumps(uJSON, indent=4)
    userJSON = jsonpickle.decode(userJSONData)
    userJSON = json.loads(userJSON) 

    return jsonify({'users': userJSON})

# Get one user #
#################
def getSpecificUser(id):
    users = USER.query.filter_by(id=id).first()

    if users:
        uJSON = jsonpickle.encode(users, unpicklable=False) 
        userJSONData = json.dumps(uJSON, indent=4)
        userJSON = jsonpickle.decode(userJSONData)
        userJSON = json.loads(userJSON) 
        return jsonify({'users': userJSON})
    else:
        abort(404)

# Delete one user #
###################
def deleteSpecificUser(id):
    users = USER.query.filter_by(id=id).first()
    if users:
        USER.query.filter_by(id=id).delete()
        db.session.commit()
        return provideGenericSuccess()
    else:
        abort(404)

# Update one user #
###################
def updateSpecificUser(id, req):
    user = USER.query.filter_by(id=id).first()
    if user:
            # Todo? Check why this doesn't work...
                # if type(req['firstName']) != unicode:
                #     abort(400)
                # else:

        # Specific Column Validations #
        if 'firstName' in req:
                user.firstName = req['firstName']
        if 'lastName' in req:
                user.lastName = req['lastName']
        if 'jobTitle' in req:
                user.jobTitle = req['jobTitle']
        if 'email' in req:
                user.email = req['email']
        if 'password' in req:
                user.password = bcrypt.generate_password_hash(req['password'])
        if 'isActive' in req:
                user.isActive = req['isActive']
        if 'isPwdExp' in req:
                user.isPwdExp = req['isPwdExp']

        db.session.commit()
        return provideGenericSuccess()
    else:
        abort(404)

# Add a User #
##############
def addUser(req):
    user = USER()
    for items in req:
        if items == 'firstName':
            user.firstName = req['firstName']
        if items == 'lastName':
            user.lastName = req['lastName']
        if items == 'jobTitle':
            user.jobTitle = req['jobTitle']
        if items == 'email':
            user.email = req['email']
            emailCheck = USER.query.filter_by(email=user.email).first()
            if emailCheck:
                return make_response(jsonify({'response': 'email already exists'}), 400)
        if items == 'password':
            user.password = bcrypt.generate_password_hash(req['password'])
        if items == 'manager':
            user.manager = req['manager']
        if items == 'accessLevel':
            user.accessLevel = req['accessLevel']
        if items == 'deactivateDate':
            retDate = datetime.strptime(req['deactivateDate'], '%y-%m-%d')
            user.deactivateDate = retDate
        if items == 'photo':
            user.photo = req['photo']
        if items == 'businessLine':
            user.businessLine = req['businessLine']
        if items == 'isPwdExp':
            user.isPwdExp = req['isPwdExp']

    db.session.add(user)
    db.session.commit()
    return provideGenericSuccess()

# Validate a user's password #
##############################
def validatePassword(email, pwd):
    user = USER.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, pwd):
        
        uJSON = jsonpickle.encode(user, unpicklable=False) 
        userJSONData = json.dumps(uJSON, indent=4)
        userJSON = jsonpickle.decode(userJSONData)
        userJSON = json.loads(userJSON) 
        return jsonify({'user': userJSON})
    else:
        return make_response(jsonify({'response': 'incorrect password'}), 400)

# Deactivate a User #
#####################
def deactivateUser(id):
    user = USER.query.filter_by(id=id).first()
    user.isActive = False
    db.session.commit()

    return provideGenericSuccess()