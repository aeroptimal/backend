from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from conf import settings

from models.model import db

def create():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = settings.SECRET_KEY
    app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USERNAME'] = settings.EMAIL_USER
    app.config['MAIL_PASSWORD'] = settings.EMAIL_PASSWORD
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return app