from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI


#  FORMAT AS USD  # 
# WHY CANT I PUT THIS IN METHODS? #
###################
def formatAsUSD(x):
    if x is None:
        return "null"
    elif x == '':
        return "null"
    else:
        return "${:,.2f}".format(x)

app.jinja_env.globals.update(usd=formatAsUSD)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
auth = HTTPBasicAuth()



from app import routes