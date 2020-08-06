from flask import flash, session, abort, request
import requests
from requests.auth import HTTPBasicAuth
import json
from datetime import datetime
from config import *

###################
#  STATUS / MISC  #
###################

#  GET STATUS OF SERVICE  #
def getStatus(site):
    endpoint = site + '/status'
    res = 'pending'

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    return res

#  VERIFY SESSION  #
def verifySession():
    if 'isLoggedIn' in session and 'currentUser' in session:
        return True
    elif request.remote_addr == '127.0.0.1':
        return True
    else:
        return False

#  FORMAT AS USD  #
def formatAsUSD(x):
    if x is None:
        return "null"
    elif x == '':
        return "null"
    else:
        return "${:,.2f}".format(x)


##############################
#  AUTHENTICATION FUNCTIONS  #
##############################

#  GET USER NAME BY ID  #
def getUserNameByID(id):
    endpoint = SERVICE_ADDRESSES['auth']+'/api/v1.0/users/'+str(id)

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]
            return childItem['firstName'] + " " + childItem['lastName']           
    else:
        return "Error in function getUserByID."

#  AUTHENTICATE USER  #
def authenticateUser(email, pwd):
    endpoint = SERVICE_ADDRESSES['auth']+'/api/v1.0/users/session'

    obj = {'email':email, 'password':pwd}

    try:
        res = requests.post(endpoint, json=obj, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:

            if resDict[item] == 'incorrect password':
                return 'failure'

            else:
                user = resDict[item]
                retDict = {}

                for attr in user:
                    retDict[attr] = user[attr]
                    print (retDict[attr])

                if retDict['isActive'] == False:
                    return 'inactive'
                else:
                    if 'isLoggedIn' not in session:
                        session['currentUser'] = retDict
                        session['isLoggedIn'] = True

                print(retDict)
                return 'success'
        else:
            return 'failure'

#  ADD USER  #
def addUser(obj):
    endpoint = SERVICE_ADDRESSES['auth']+'/api/v1.0/users/add'

    try:
        res = requests.post(endpoint, json=obj, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]
            print(childItem)
            return childItem #return response
    else:
        return "failure"

#  UPDATE PASSWORD  #
def updatePassword(id, pwd):
    endpoint = SERVICE_ADDRESSES['auth']+'/api/v1.0/users/' + str(id)

    obj = {'password':pwd}

    try:
        res = requests.put(endpoint, json=obj, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]
            print(childItem)
            return childItem #return response
    else:
        return "failure"

#  DEACTIVATE USER  #
def updateUserActivation(id, status):
    endpoint = SERVICE_ADDRESSES['auth']+'/api/v1.0/users/' + str(id)

    obj = {}
    if status == False:
        obj = {'isActive':status}
    else:
        obj = {'isActive':status, 'isPwdExp':False}

    try:
        res = requests.put(endpoint, json=obj, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]
            print(childItem)
            return childItem #return response
    else:
        return "failure"  

###########################
#  OPPORTUNITY FUNCTIONS  #
###########################

#  FETCH ALL OPPORTUNITIES  #
def getOpportunities():
    opps = [{}]
    endpoint = SERVICE_ADDRESSES['opp']+'/api/v1.0/opp'

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"
    
    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]

            for attr in childItem:
                opp = {}
                opp['id'] = attr['id']
                opp['customerName'] = attr['customerName'] 
                opp['desc'] = attr['desc']         
                opp['contractTerm'] = attr['contractTerm'] 
                opp['requestOwner'] = getUserNameByID(attr['requestOwner'])
                #opp['requestTeam'] = attr['requestTeam'] 
                opp['requestStatus'] = attr['requestStatus']
                opp['lastModified'] = attr['lastModified'][0:attr['lastModified'].find('T')]
                opp['createdDate'] = attr['createdDate'][0:attr['createdDate'].find('T')]
                opp['tcv'] = attr['tcv']         
                opp['bundle'] = attr['bundle']

                opps.append(opp)
        return opps
    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"

#  FETCH OPPORTUNITY  #
def getOpportunity(id):
    opp = {}
    endpoint = SERVICE_ADDRESSES['opp']+'/api/v1.0/opp/'+str(id)

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()

        if 'response' in resDict:
            if resDict['response'] == 'not found':
                abort(404)
        else:
            for item in resDict:
                childItem = resDict[item]
                opp['id'] = childItem['id']
                opp['customerName'] = childItem['customerName']
                opp['desc'] = childItem['desc']
                opp['contractTerm'] = childItem['contractTerm']
                opp['requestOwner'] = getUserNameByID(childItem['requestOwner'])
                opp['requestStatus'] = childItem['requestStatus']
                opp['lastModified'] = childItem['lastModified'][0:childItem['lastModified'].find('T')]
                opp['createdDate'] = childItem['createdDate'][0:childItem['createdDate'].find('T')]
                opp['tcv'] = childItem['tcv']
                opp['bundle'] = childItem['bundle']
        
            return opp
    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"

#  CREATE OPPORTUNITY  #
def createOpportunity(opp):
    endpoint = SERVICE_ADDRESSES['opp']+'/api/v1.0/opp'
    opp['contractTerm'] = DEFAULT_CONTRACT_TERM

    try:
        res = requests.post(endpoint, json=opp, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    print (res)
    return res

#  UPDATE OPPORTUNITY  #
def updateOpportunity(opp_id, opp):
    endpoint = SERVICE_ADDRESSES['opp']+'/api/v1.0/opp/' + str(opp_id)
    
    try:
        res = requests.put(endpoint, json=opp, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]
            return childItem #return response

#  DELETE OPPORTUNITY  #
def deleteOpportunity(opp_id):
    endpoint = SERVICE_ADDRESSES['opp']+'/api/v1.0/opp/' + str(opp_id)
    
    try:
        res = requests.delete(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]
            return childItem #return response

#  GET # OF OPPORTUNITIES PER STATUS  #
def getNumOfOppsByStatus(status):
    opps = getOpportunities()
    count = 0
    for opp in opps:
        if 'requestStatus' in opp:
            if opp['requestStatus'] == status:
                count = count + 1
    return count

#  GET DOCUMENT  #
def generateDocument(obj, doc_id):
    endpoint = SERVICE_ADDRESSES['doc']+'/api/v1.0/doc/'+ str(doc_id)

    try:
        res = requests.post(endpoint, json=obj, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        return res.content

    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"

#  HAS DOCUMENT BEEN CREATED  #
def verifyDocFile(opp_id):
    import os.path
    from os import path

    if path.exists('app/pdf/' + str(opp_id) + '.pdf'):
        return True
    else:
        return False


###################
#  LINE FUNCTIONS #
###################

#  DELETE LINE ITEM  #
def deleteLine(opp_id, line_id):
    endpoint = SERVICE_ADDRESSES['opp']+'/api/v1.0/opp/'+str(opp_id)+'/bundle/'+str(line_id)
    
    try:
        res = requests.delete(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            childItem = resDict[item]
            return childItem #return response

#  GET PRODUCT FAMILIES  #
def getProductFamilies():
    families = []
    endpoint = SERVICE_ADDRESSES['prod']+'/api/v1.0/prod/families'

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            return resDict[item]
        
    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"

#  GET MODELS BY FAMILY  #
def getModelsByFamily(family):
    endpoint = SERVICE_ADDRESSES['prod']+'/api/v1.0/prod/'+family+'/models'

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        for item in resDict:
            return resDict[item]
        
    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"

#  GET MODELS  #
def getModel(family, model):
    endpoint = SERVICE_ADDRESSES['prod']+'/api/v1.0/prod/'+family+'/'+model

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        retDict = {}
        for item in resDict:
            retDict[item] = resDict[item]
        return retDict
        
    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"

#  GET ALL PARTS  #
def queryAllParts(family, model):
    endpoint = SERVICE_ADDRESSES['prod']+'/api/v1.0/prod/'+family+'/'+model+'/parts'

    try:
        res = requests.get(endpoint, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        resDict = res.json()
        arrParts = []

        for item in resDict:
            lineDict = resDict[item]

            for child in lineDict:
                arrParts.append(child)
            
        return arrParts
        
    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"

#  ADD LINES  #
def addLines(opp_id, bundle):
    endpoint = SERVICE_ADDRESSES['opp']+'/api/v1.0/opp/'+ str(opp_id) +'/bundle'

    print(bundle)

    try:
        res = requests.post(endpoint, json=bundle, auth=HTTPBasicAuth(INT_USER, INT_PASS))
    except requests.exceptions.ConnectionError:
        res = "down"

    if res != "down":
        print(res)
        return "success"
        
    else:
        flash(f'Opportunity Service is down!', 'danger')
        return "error"