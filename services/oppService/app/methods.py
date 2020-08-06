from app import db, bcrypt
from flask import jsonify, abort, redirect, url_for, make_response
from app.models import OPP
import json
import jsonpickle
from json import JSONEncoder
from datetime import datetime, date

# Provide Generic Success #
###########################
def provideGenericSuccess():
    return jsonify({'response': 'success'})

# Get all opps  #
#################
def getAllOpps():
    opps = OPP.query.all()
    oJSON = jsonpickle.encode(opps, unpicklable=False) 
    oppJSONData = json.dumps(oJSON, indent=4)
    oppJSON = jsonpickle.decode(oppJSONData)
    oppJSON = json.loads(oppJSON) 

    return jsonify({'opportunities': oppJSON})

# Get one opp   #
#################
def getSpecificOpp(id):
    opp = OPP.query.filter_by(id=id).first()

    if opp:
        oJSON = jsonpickle.encode(opp, unpicklable=False) 
        oppJSONData = json.dumps(oJSON, indent=4)
        oppJSON = jsonpickle.decode(oppJSONData)
        oppJSON = json.loads(oppJSON) 
        return jsonify({'opportunity': oppJSON})
    else:
        abort(404)

# Delete one opp  #
###################
def deleteSpecificOpp(id):
    users = OPP.query.filter_by(id=id).first()
    if users:
        OPP.query.filter_by(id=id).delete()
        db.session.commit()
        return provideGenericSuccess()
    else:
        abort(404)

# Update one Opp #
###################
def updateSpecificOpp(id, req):
    opp = OPP.query.filter_by(id=id).first()
    if opp:

        # Specific Column Validations #
        if 'customerName' in req:
                opp.customerName = req['customerName']
        if 'desc' in req:
                opp.desc = req['desc']
        if 'contractTerm' in req:
                opp.contractTerm = req['contractTerm']
        if 'requestOwner' in req:
                opp.requestOwner = req['requestOwner']
        if 'requestStatus' in req:
                opp.requestStatus = req['requestStatus']
        if 'lastModified' in req:
                opp.lastModified = req['lastModified']
        if 'tcv' in req:
                opp.tcv = req['tcv']
        if 'bundle' in req:
                opp.bundle = req['bundle']

        opp.lastModified = date.today()

        db.session.commit()
        return provideGenericSuccess()
    else:
        abort(404)

# Add a Opp #
##############
def addOpp(req):
    opp = OPP()   

    for items in req:
        if items == 'customerName':
            opp.customerName = req['customerName']
        if items == 'desc':
            opp.desc = req['desc']
        if items == 'contractTerm':
            opp.contractTerm = req['contractTerm']
        if items == 'requestOwner':
            opp.requestOwner = req['requestOwner']
        if items == 'requestStatus':
            opp.requestStatus = req['requestStatus']
        if items == 'tcv':
            opp.tcv = req['tcv']
        if items == 'bundle':
            opp.bundle = req['bundle']

    db.session.add(opp)
    db.session.commit()
    return provideGenericSuccess()

# Get Line Items #
##################
def getBundle(id):
    opp = OPP.query.filter_by(id=id).first()

    if opp:
        return opp.bundle
    else:
        abort(404)

# Add a Line Item #
###################
def addLines(id, req):
    opp = OPP.query.filter_by(id=id).first()
    if opp:
        parent = {}
        arrLines = [] 

        if opp.bundle is not None and opp.bundle != '' and opp.bundle != ' ':
            currentBundle = json.loads(opp.bundle)    # Load JSON string from DB into Json Object

            # LOOP CURRENT ITEMS   #
            #########################
            for lines in currentBundle:               # This specific Line
                child = currentBundle[lines]
                childDict = {}

                for attr in child:                    # Loop every attribute #
                    childDict[attr] = child[attr]

                arrLines.append(childDict)            # Append to the master list #

        #   LOOP NEW ITEMS       #
        ##########################                # Same operation as above, but do it on the 'new' items.
        for lines in req:
            child = req[lines]              
            childDict = {}

            for attr in child:              
                childDict[attr] = child[attr]

            arrLines.append(childDict)      

        #   PROCESS WHOLE LIST   #
        ##########################
        x = 0
        for line in arrLines:
            parent[x] = arrLines[x]
            x = x + 1

        invJson = json.dumps(parent)               # Make JSON String #
        opp.bundle = invJson

    else:
        abort(404)

    db.session.commit()
    return provideGenericSuccess()

# Delete a Line Item #
######################
def deleteLine(id, lineId):
    opp = OPP.query.filter_by(id=id).first()

    if opp:
        parent = {}
        arrLines = [] 

        currentBundle = json.loads(opp.bundle)    # Load JSON string from DB into Json Object #

        # LOOP CURRENT ITEMS   #
        #########################
        for lines in currentBundle:               # This specific Line #
            child = currentBundle[lines]
            childDict = {}

            if lines != str(lineId):                  # If the line is not to be deleted #
                for attr in child:                    # Loop every attribute #
                    childDict[attr] = child[attr]
                arrLines.append(childDict)            # Append to the master list #

        #   PROCESS WHOLE LIST   #
        ##########################
        x = 0
        for line in arrLines:
            parent[x] = arrLines[x]
            x = x + 1

        invJson = json.dumps(parent)               # Make JSON String #
        opp.bundle = invJson

    else:
        abort(404)

    db.session.commit()
    return provideGenericSuccess()

# Update a Line Item #
######################
def updateLine(id, lineId, req):
    opp = OPP.query.filter_by(id=id).first()

    if opp:
        parent = {}
        arrLines = [] 

        currentBundle = json.loads(opp.bundle)        # Load JSON string from DB into Json Object #

        # LOOP CURRENT ITEMS   #
        #########################
        for lines in currentBundle:                   # This specific Line #
            child = currentBundle[lines]
            childDict = {}

            if lines == str(lineId):                  # If the line is not to be deleted #
                for attr in child:                    # Loop every attribute #
                    if attr in req:
                        childDict[attr] = req[attr]
                    else:
                        childDict[attr] = child[attr]
                arrLines.append(childDict)            # Append to the master list #

        #   PROCESS WHOLE LIST   #
        ##########################
        x = 0
        for line in arrLines:
            parent[x] = arrLines[x]
            x = x + 1

        invJson = json.dumps(parent)               # Make JSON String #
        opp.bundle = invJson

    else:
        abort(404)

    db.session.commit()
    return provideGenericSuccess()