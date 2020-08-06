from flask import *
from app import app, db, auth
from app.models import OPP
from app.methods import *
from config import *
from datetime import datetime

# STATUS PAGES #
###############
@app.route("/status")
def home():
    return jsonify({'status': 'up'})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'response': 'not found'}), 404)

# API Routes #
##############
@app.route('/api/v1.0/opp', methods=['GET'])
@auth.login_required
def get_opps():
    return getAllOpps()

@app.route('/api/v1.0/opp/<int:opp_id>', methods=['GET'])
@auth.login_required
def get_opp(opp_id):
    return getSpecificOpp(opp_id)

@app.route('/api/v1.0/opp/<int:opp_id>', methods=['DELETE'])
@auth.login_required
def delete_opp(opp_id):
    return deleteSpecificOpp(opp_id)

@app.route('/api/v1.0/opp/<int:opp_id>', methods=['PUT'])
@auth.login_required
def update_opp(opp_id):
    if not opp_id:
        abort(404)
    if not request.json:
        abort(400)
    return updateSpecificOpp(opp_id, request.json)

@app.route('/api/v1.0/opp', methods=['POST'])
@auth.login_required
def add_opp():
    if not request.json:
        abort(400)
    if 'customerName' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)
    if 'contractTerm' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)
    if 'requestOwner' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)
    return addOpp(request.json)

@app.route('/api/v1.0/opp/<int:opp_id>/bundle', methods=['GET'])
@auth.login_required
def get_bundle(opp_id):
    return getBundle(opp_id)

@app.route('/api/v1.0/opp/<int:opp_id>/bundle', methods=['POST'])
@auth.login_required
def add_bundle(opp_id):
    if not request.json:
        abort(400)
    return addLines(opp_id, request.json)

@app.route('/api/v1.0/opp/<int:opp_id>/bundle/<int:line_id>', methods=['DELETE'])
@auth.login_required
def delete_line_item(opp_id, line_id):
    if not opp_id:
        abort(400)
    if not str(line_id):
        abort(400)
    return deleteLine(opp_id, line_id)

@app.route('/api/v1.0/opp/<int:opp_id>/bundle/<int:line_id>', methods=['PUT'])
@auth.login_required
def update_line_item(opp_id, line_id):
    if not opp_id:
        abort(400)
    if not request.json:
        abort(400)
    return updateLine(opp_id, line_id, request.json)


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