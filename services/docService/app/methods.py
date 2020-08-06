from app import db, bcrypt
from flask import jsonify, abort, redirect, url_for, make_response
from app.models import *
import json
import jsonpickle
from json import JSONEncoder
from datetime import datetime, date
import random
import string
from config import *

# Provide Generic Success #
###########################
def provideGenericSuccess():
    return jsonify({'response': 'success'})

# Validate Payload #
####################
def validateRequest(obj):

    arrRequiredKeys = ['id', 'customerName', 'desc', 'contractTerm', 'requestOwner', 'lastModified', 'bundle']
    for key in arrRequiredKeys:
        if key not in obj:
            return False

    return True


