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
@app.route("/api/v1.0/doc/<int:template>", methods=['POST'])
@auth.login_required
def getDocument(template):

    # HEADER HANDLE #
    #################
    if not request.json:
        print("err1")
        abort(404)

    if validateRequest(request.json) == False:
        print("err2")
        abort(400)

    header = request.json

    # LINE ITEMS #
    ##############
    arrDistinctPNs = []
    arrLines = []
    bundle = json.loads(header['bundle'])

    for item in bundle:
        child = bundle[item]
        pn = child['partNumber']
        arrLines.append(child)

        if pn not in arrDistinctPNs:
            arrDistinctPNs.append(pn)

    # DETERMINE TERMS #
    ###################
    arrTerms = []
    qryTerms = TERMS.query.all()

    for terms in qryTerms:
        isEnabled = False

        if terms.enabledPNs == "ALL":
            isEnabled = True
        else:
            arrEnabledPNs = terms.enabledPNs.split("#")
            for pn in arrDistinctPNs:
                if pn in arrEnabledPNs:
                    isEnabled = True

        if isEnabled:
            f = open(terms.template, 'r')
            contents = f.read()
            arrTerms.append(contents)

    doc = DOCUMENT.query.filter_by(id=template).first()
    return render_template(doc.template, header=header, terms=arrTerms, lines=arrLines)

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