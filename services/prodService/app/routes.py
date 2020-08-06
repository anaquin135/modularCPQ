from flask import *
from app import app, db, auth
from app.models import *
from app.methods import *
from config import *
from datetime import datetime

# STATUS PAGES #
################
@app.route("/status")
def home():
    return jsonify({'status': 'up'})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'response': 'not found'}), 404)

# API Routes #
##############
@app.route("/api/v1.0/prod/families")
@auth.login_required
def getFamilies():
    ret = {
        "Product Families":getProductFamilies()
    }
    return jsonify(ret)

@app.route("/api/v1.0/prod/<string:family>/models")
@auth.login_required
def getModels(family):
    return jsonify (getProductModels(family))

@app.route("/api/v1.0/prod/<string:family>/<string:model>")
@auth.login_required
def getSpecificModel(family, model):
    return jsonify (queryModel(model))


@app.route("/api/v1.0/prod/<string:family>/<string:model>/attr")
@auth.login_required
def getAttributes(family, model):
    return jsonify(getAttributeDefinitions(model))

@app.route("/api/v1.0/prod/<string:family>/<string:model>/attr/parts")
@auth.login_required
def getPartsByAttr(family, model):
    if not request.json:
        abort(404)
    res = queryPartsByAttribute(model, request.json['attr1'], request.json['attr2'], request.json['attr3'], request.json['attr4'], request.json['attr5'])
    return jsonify(res)

@app.route("/api/v1.0/prod/<string:family>/<string:model>/parts")
@auth.login_required
def getPartsByModel(family, model):
    res = queryPartsByModel(model)
    return jsonify(res)

# SERVICE AUTH #
################
@auth.get_password
def get_password(username):
    if username == INT_USER:
        return INT_PASS
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403) #401)