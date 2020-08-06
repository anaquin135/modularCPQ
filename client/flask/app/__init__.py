from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_httpauth import HTTPBasicAuth
from app.methods import formatAsUSD
from config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.jinja_env.globals.update(usd=formatAsUSD) # This 'formatAsUSD' function is in the methods file.

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from app import routes