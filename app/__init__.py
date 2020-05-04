from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_login import LoginManager
from flask_session import Session
import os
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/caremax'
app.config['SQLALCHEMY_TRACK_MIDIFICATION'] = False
app.config['SECRET_KEY'] = 'thisismysecretkey'

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)
login_manager.login_message_category = 'info'


from app import views
from app import models
from app import forms
from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))











