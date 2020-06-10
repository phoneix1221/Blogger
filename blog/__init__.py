from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import pytz
from flask_bcrypt import Bcrypt
from mailjet_rest import Client
import os
 
app = Flask(__name__,static_url_path='/static')

app.config["CACHE_TYPE"] = "null"
app.config['SECRET_KEY']='b906f7ba0889aaaec7190df644320452'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'
from blog import routes

