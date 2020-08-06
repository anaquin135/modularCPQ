from flask import *
from app import app, db, auth
from app.models import USER
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
@app.route('/api/v1.0/users', methods=['GET'])
@auth.login_required
def get_users():
    return getAllUsers()

@app.route('/api/v1.0/users/<int:user_id>', methods=['GET'])
@auth.login_required
def get_user(user_id):
    return getSpecificUser(user_id)

@app.route('/api/v1.0/users/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    return deleteSpecificUser(user_id)

@app.route('/api/v1.0/users/<int:user_id>', methods=['PUT'])
@auth.login_required
def update_user(user_id):
    if not user_id:
        abort(404)
    if not request.json:
        abort(400)
    return updateSpecificUser(user_id, request.json)

@app.route('/api/v1.0/users/add', methods=['POST'])
@auth.login_required
def add_user():
    if not request.json:
        abort(400)

    if 'firstName' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)
    if 'lastName' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)
    if 'jobTitle' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)
    if 'email' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)
    if 'password' not in request.json:
        return make_response(jsonify({'response': 'missing key'}), 400)

    return addUser(request.json)

@app.route('/api/v1.0/users/session', methods=['POST'])
@auth.login_required
def login_user():
    if not request.json:
        abort(400)
    
    if 'password' in request.json and 'email' in request.json:
        return validatePassword(request.json['email'], request.json['password'])
    else:
        abort(400)

@app.route('/api/v1.0/users/script/deactivate', methods=['GET'])
@auth.login_required
def deactivate_expired():
    todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
    user = USER.query.filter(USER.deactivateDate <= todays_datetime).all()
    for users in user:
        ret = deactivateUser(users.id)

    return provideGenericSuccess()

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