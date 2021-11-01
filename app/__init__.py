from flask import Flask
from config import Config
#to log in user in and out and maintain the session
from flask_login import LoginManager
#this talks to database
from flask_sqlalchemy import SQLAlchemy
#this makes altering the database a lot easier
from flask_migrate import Migrate


# app instantiation
app = Flask(__name__)
app.config.from_object(Config)

# init Login Manager
login = LoginManager(app)
# This is where you will be sent if you are not logged in
login.login_view = 'login'

# init the database
db = SQLAlchemy(app)

# init Migrate
migrate = Migrate(app,db)

from app import routes