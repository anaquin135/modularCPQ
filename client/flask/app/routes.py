from flask import render_template, url_for, flash, redirect, request, session, send_file, send_from_directory
from app import app, bcrypt
from config import *
from app.methods import *
from app.forms import *
from datetime import date
from functools import wraps

#######################
# TRACK SERVICE STATE #
#######################
services = [
    {
        'name': 'authentication',
        'status': 'pending',
        'address': SERVICE_ADDRESSES['auth']
    },
    {
        'name': 'opportunity',
        'status': 'pending',
        'address': SERVICE_ADDRESSES['opp']
    },
    {
        'name': 'products',
        'status': 'pending',
        'address': SERVICE_ADDRESSES['prod']
    },
    {
        'name': 'document',
        'status': 'pending',
        'address': SERVICE_ADDRESSES['doc']
    }
]

############################
# LOGIN REQUIRED DECORATOR #
############################
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if verifySession() == False:
               flash(f'Login Required!', 'danger')
               return redirect(url_for('login'))

            return f(*args, **kws)            
    return decorated_function

########################
# ROUTES: Home, Status #
########################
@app.route("/")
@app.route("/home")
def home():
    if verifySession():
        user=session['currentUser']
        numOfOpen   = getNumOfOppsByStatus('In Progress')
        numOfClosed = getNumOfOppsByStatus('Closed')
        return render_template('dashboard.html', title="Dashboard", loggedIn=verifySession(), user=user, numOpen=numOfOpen, numClosed=numOfClosed)
    else:    
        return render_template('home.html', title="Homepage", loggedIn=verifySession())

@app.route("/status")
@authorize
def status():
    user=session['currentUser']

    for service in services:
        res = getStatus(service['address'])
        if res != 'down' and res != 'pending':
            service['status'] = 'up'
        else:
            service['status'] = res

    return render_template('status.html', title="Status Check", loggedIn=verifySession(), services=services, user=user)

@app.errorhandler(404)
def page_not_found(e):
    user = session['currentUser']
    return render_template('404.html', user=user, title="404", loggedIn=verifySession()), 404

########################
# ROUTES: User Routes  #
########################
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = loginForm()

    if form.validate_on_submit():
        res = authenticateUser(form.email.data, form.password.data)
        if res == 'success':
            user = session['currentUser']
            
            if user['isPwdExp'] == True:
                flash(f'Your password is expired. Please change it now! Otherwise, you will need to contact an administrator.', 'warning')
                res2 = updateUserActivation(user['id'], False)
                return redirect(url_for('changePassword'))
            else:
                flash(f'Successful Login!', 'success')
                return redirect(url_for('home'))

        elif res == 'inactive':
                flash(f'Your account is deactivated. Please contact an administrator!', 'danger')
                return redirect(url_for('login'))

        else:
            flash(f'Unsuccessful Login.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', title="Login", form=form, loggedIn=verifySession())

@app.route("/logout")
def logout():
    
    session.pop('currentUser', None)
    session.pop('isLoggedIn', None)
    flash(f'Successfully Logged out!', 'success')
    return redirect(url_for('login'))
    #return render_template('logout.html', title="Logging Out...", form=form, loggedIn=verifySession())

@app.route("/register", methods=['GET', 'POST'])
@authorize
def register():
    user=session['currentUser']

    if user['accessLevel'] != 2:
        flash(f"You do not have the proper access level for this!")
        return(redirect(url_for('home')))
    else:
        form = addUserForm()
        if form.validate_on_submit():
            obj = {}
            obj['firstName']    = form.firstName.data
            obj['lastName']     = form.lastName.data  
            obj['email']        = form.email.data      
            obj['jobTitle']     = form.jobTitle.data            
            obj['isActive']     = form.isActive.data           
            obj['accessLevel']  = form.accessLevel.data                                
            obj['businessLine'] = form.businessLine.data
            obj['password']     = form.password.data
            obj['isPwdExp']     = True

            res = addUser(obj)
            if res == "success":
                flash(f'Success! User has been created.', 'success')
                return redirect(url_for('home'))

        return render_template('register.html', title="Register", form=form, loggedIn=verifySession(), user=user)

@app.route("/profile")
@authorize
def profile():
    # WIP
    user=session['currentUser']
    return render_template('profile.html', title="Profile", loggedIn=verifySession(), user=user)

@app.route("/changepwd", methods=['GET', 'POST'])
@authorize
def changePassword():

    user = session['currentUser']
    form = changePassForm()

    if form.validate_on_submit():
        if form.password.data != form.confirmPassword.data:
            flash(f'New passwords do not match.', 'danger')
            return redirect(url_for('changePassword'))
        else:
            res = authenticateUser(user['email'], form.currentPassword.data)
            if res == 'success' or res == 'inactive':
                result = updatePassword(user['id'], form.password.data)
                if result == 'success':
                    flash(f'Password changed successfully!', "success")
                    updateUserActivation(user['id'], True)
                    session.pop('currentUser', None)
                    session.pop('isLoggedIn', None)
                    return(redirect(url_for('login')))
                else:
                    flash(f'Password changed failed!', "danger") 
                    return(redirect(url_for('changePassword')))   
            else:
                flash(f'Current Password Does Not Match!', "danger") 
                return(redirect(url_for('changePassword')))              

    return render_template('change-pass.html', title="Profile", form=form, loggedIn=verifySession(), user=user)

########################
# ROUTES: Opportunity  #
########################
@app.route("/inbox")
@authorize
def inbox():
    user = session['currentUser']
    opps = getOpportunities()
    return render_template('inbox.html', title="Opportunities", loggedIn=verifySession(), opps=opps, user=user)

@app.route("/create", methods=['GET', 'POST'])
@authorize
def createNew():
    user = session['currentUser']
    form = newOpportunity()
    if form.validate_on_submit():
        opp = {}
        opp['customerName'] = form.customerName.data
        opp['desc'] = form.desc.data
        opp['requestOwner'] = user['id']
        createOpportunity(opp)
        flash(f'Opportunity Created!', 'success')
        return(redirect(url_for('inbox')))

    return render_template('create-new.html', title="Create New", loggedIn=verifySession(), form=form, user=user, today=date.today())

@app.route("/opp/<int:opp_id>/delete", methods=['GET', 'POST'])
@authorize
def deleteOpp(opp_id):
    opp = getOpportunity(opp_id)
    user = session['currentUser']
    form = getConfirmationForm()

    if form.validate_on_submit():
        if (user['id'] != opp['requestOwner']) and user['accessLevel'] == 1:
            flash(f'Only the request owner may delete their opportunity!', 'danger')
            return(redirect(url_for('inbox')))
        else:
            res = deleteOpportunity(opp_id)
            flash(f'Opportunity successfully deleted!', 'success')
            return(redirect(url_for('inbox')))

    return render_template('delete.html', title="Delete Opportunity", loggedIn=verifySession(), user=user, opp=opp, form=form)

@app.route("/opp/<int:opp_id>/close", methods=['GET'])
@authorize
def closeOpp(opp_id):
    if verifyDocFile(opp_id) == False:
        flash(f'There is no quote attached to this opportunity. Maybe you should generate one before closing it.', 'warning')
        return redirect(url_for('opportunity', opp_id=opp_id))
    else:
        opp = getOpportunity(opp_id)
        opp['requestStatus'] = 'Closed'
        opp.pop('requestOwner')

        res = updateOpportunity(opp_id, opp)
        flash(f'Success, the opportunity has been closed.', 'success')
        return redirect(url_for('opportunity', opp_id=opp_id))

# Primary Opportunity Viewing Route #
@app.route("/opp/<int:opp_id>", methods=['GET', 'POST', 'DELETE'])
@authorize
def opportunity(opp_id):
    user = session['currentUser']
    opp = getOpportunity(opp_id)
    form = opportunitySave()

    # PROCESS LINE ITEMS #
    ######################
    lineItems = []

    if opp['bundle'] != '' and opp['bundle'] != None:
        jsonBundle = json.loads(opp['bundle'])
        for items in jsonBundle:
            child = jsonBundle[items]
            item = {}
            item['id'] = items
            
            for attr in child:
                item[attr] = child[attr]

            lineItems.append(item)

    #  SAVE REQUEST #
    #################
    if request.method == "POST":
        if form.validate_on_submit():

            # PROCESS HEADER #
            ##################
            newOpp = {}
            newOpp['customerName'] = form.customerName.data
            newOpp['desc']         = form.desc.data
            newOpp['contractTerm'] = form.contractTerm.data

            # PROCESS LINES  #
            ##################
            x = 0
            parent = {}

            sumExtMRC = 0
            sumExtNRC = 0
            for line in lineItems:
                line['qtyNew'] = request.form[line['id']+'-qtyNew']
                line['qtyExi'] = request.form[line['id']+'-qtyExi']
                line['discNRC'] = request.form[line['id']+'-discNRC']
                line['discMRC'] = request.form[line['id']+'-discMRC']

                ### QUICK FIN. CALCS ###
                ########################
                line['netMRC'] = (line['listMRC'] * (1 - float(line['discMRC'])))
                line['netNRC'] = (line['listNRC'] * (1 - float(line['discNRC'])))

                line['extMRC'] = (line['netMRC'] * (int(line['qtyNew']) + int(line['qtyExi'])))
                line['extNRC'] = (line['netNRC'] * (int(line['qtyNew'])))

                sumExtMRC = line['extMRC'] + sumExtMRC
                sumExtNRC = line['extNRC'] + sumExtNRC

                parent[str(x)] = line
                x = x + 1

            # TCV #
            if newOpp['contractTerm'] != 0:
                newOpp['tcv'] = (sumExtMRC * newOpp['contractTerm']) + sumExtNRC
            else:
                newOpp['tcv'] = (sumExtMRC * 1) + sumExtNRC

            newBundle = json.dumps(parent)
            newOpp['bundle'] = newBundle

            res = updateOpportunity(opp_id, newOpp)
            if res == "success":
                flash(f'Save successful!', 'success')
                return redirect(url_for('opportunity', opp_id=opp_id))

    if (opp['requestStatus'] == "Closed"):
            return render_template('opp-readonly.html', title="Opportunity View", loggedIn=verifySession(), user=user, opp=opp, form=form, lineItems=lineItems, docExists=verifyDocFile(opp_id))
    else:
        return render_template('opp.html', title="Opportunity View", loggedIn=verifySession(), user=user, opp=opp, form=form, lineItems=lineItems, docExists=verifyDocFile(opp_id))

@app.route("/opp/<int:opp_id>/line/<int:line_id>/delete", methods=['GET', 'POST'])
@authorize
def deleteLineFromBundle(opp_id, line_id):
    res = deleteLine(opp_id, line_id)

    if res == 'success':
        flash(f'Line successfully deleted!', 'success')
        return(redirect(url_for('opportunity', opp_id=opp_id)))
    else:
        flash(f'There was an error!', 'danger')
        return(redirect(url_for('opportunity', opp_id=opp_id)))

#########################
# ROUTES: Configuration #
#########################
@app.route("/opp/<int:opp_id>/line/add", methods=['GET', 'POST'])
@authorize
def selectFamily(opp_id):
    opp = getOpportunity(opp_id)
    user = session['currentUser']
    arrFamilies = getProductFamilies()

    return render_template('add-selectFamily.html', title="Select Product Family", loggedIn=verifySession(), user=user, opp=opp, arrFamilies=arrFamilies, opp_id=opp_id)

@app.route("/opp/<int:opp_id>/line/add/<string:family>", methods=['GET', 'POST'])
@authorize
def selectModel(opp_id, family):
    opp = getOpportunity(opp_id)
    user = session['currentUser']
    arrModels = getModelsByFamily(family)

    return render_template('add-selectModel.html', title="Select Product Model", loggedIn=verifySession(), user=user, opp=opp, family=family, arrModels=arrModels, opp_id=opp_id)

@app.route("/opp/<int:opp_id>/line/add/<string:model>/simpleconfig", methods=['GET', 'POST'])
@authorize
def simpleConfig(opp_id, model):
    opp = getOpportunity(opp_id)
    user = session['currentUser']
    modelDict = getModel('ALL', model)
    parts = queryAllParts('ALL', model)
    form = getConfirmationForm()

    if request.method == "POST":
        if form.validate_on_submit():
            arrPartsToAdd = []

            # PROCESS FORM #
            for part in parts:
                qtyNew = request.form[part['partNum']+'-qtyNew']
                qtyExi = request.form[part['partNum']+'-qtyExi']

                if qtyNew.isnumeric() == False or qtyExi.isnumeric() == False:
                    flash(f'Only numbers are permitted!', 'danger')
                    return redirect(url_for('simpleConfig', opp_id=opp_id, model=model))

                if int(qtyNew) > 0 or int(qtyExi) > 0:
                    part['qtyNew'] = qtyNew
                    part['qtyExi'] = qtyExi
                    part['partNumber'] = part['partNum']

                    ### QUICK FIN. CALCS ###
                    ########################
                    part['netMRC'] = part['listMRC']
                    part['netNRC'] = part['listNRC']
                    part['discMRC'] = 0.0
                    part['discNRC'] = 0.0
                    
                    part['extMRC'] = (part['netMRC'] * (int(part['qtyNew']) + int(part['qtyExi'])))
                    part['extNRC'] = (part['netNRC'] * (int(part['qtyNew'])))

                    arrPartsToAdd.append(part)

            # LOOP ITEMS AND ADD THEM #
            x = 0
            bundle = {}
            for part in arrPartsToAdd:
                bundle[str(x)] = part
                x = x + 1
            
            res = addLines(opp_id, bundle)
            if res == 'success':
                flash(f'Items added!', 'success')
                return redirect(url_for('opportunity', opp_id=opp_id))
                

    return render_template('add-simpleConfig.html', title="Select Product Lines", loggedIn=verifySession(), user=user, opp=opp, opp_id=opp_id, model=modelDict, parts=parts, form=form)

#################
# ROUTES: Quote #
#################
@app.route("/opp/<int:opp_id>/doc/<int:doc_id>", methods=['GET', 'POST'])
@authorize
def goGetDocument(opp_id, doc_id):
    opp = getOpportunity(opp_id)
    #user = session['currentUser']
    res = generateDocument(opp, doc_id)
    return res

@app.route("/opp/<int:opp_id>/doc/<int:doc_id>/file", methods=['GET', 'POST'])
@authorize
def goGetDocumentFile(opp_id, doc_id):
    import pdfkit
    opp = getOpportunity(opp_id)
    #user = session['currentUser']
    fn = str(opp['id']) + '.pdf'
    resFile = pdfkit.from_url('http://127.0.0.1:5000/'+url_for('goGetDocument', opp_id=opp_id, doc_id=doc_id), 'app/pdf/'+fn)
    while resFile is None:
        pass
    return send_file('pdf/'+fn, as_attachment=True, attachment_filename=fn)

@app.route("/opp/<int:opp_id>/doc/fileExisting", methods=['GET', 'POST'])
@authorize
def goGetDocumentFileExisting(opp_id):
    if verifyDocFile(opp_id) == True:
        return send_file('pdf/'+str(opp_id)+'.pdf', as_attachment=True, attachment_filename=str(opp_id)+'.pdf')
    else:
        abort(404)