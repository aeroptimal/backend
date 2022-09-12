from lib2to3.pgen2 import token
from flask import Response, render_template, current_app
from flask_mail import Mail, Message
import json
import jwt
import bcrypt
import datetime

from conf import settings
from models.model import User, db

class PasswordRestore:
    def __init__(self, params, token):
        self.params = params
        self.token = token
    
    def execute(self):
        try:
            id = jwt.decode(self.token,settings.SECRET_KEY,algorithms=["HS256"])
        except:
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        if not id.get('type') == 'reset':
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        id = id['id']
        hashed = bcrypt.hashpw(self.params.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = User.query.filter_by(id=id).first()
        query.password = hashed
        query.active = True
        db.session.commit()
        return Response(response=json.dumps({}), status=200, mimetype='application/json')

class PasswordReset:
    def __init__(self, params):
        self.params = params

    def execute(self):
        query = User.query.filter_by(email = self.params["email"]).first()
        if query:
            token = jwt.encode({"id":query.id,"type":"reset", "exp": datetime.datetime.now() + datetime.timedelta(minutes=15)},settings.SECRET_KEY,algorithm="HS256")
            with current_app.app_context():
                mail = Mail()
                msg = Message('Activation Request',
                                sender=("AeroOptimal",settings.EMAIL_USER),
                                recipients = [self.params.get('email').lower().replace(' ','')], 
                                )
                msg.html = render_template('email.html',title=f"Hello {query.name}",content=f"Reset your password here:",a_name="Activate",a=f"{settings.DOMAIN}/reset?token={token}")
                mail.send(msg)
            return Response(response=json.dumps({}), status=200, mimetype='application/json')
        else:
            return Response(response=json.dumps({"error":"Not found email"}), status=400, mimetype='application/json')

class PasswordResult:
    def __init__(self, params, token):
        self.params = params
        self.token = token

    def execute(self):
        try:
            id = jwt.decode(self.token,settings.SECRET_KEY,algorithms=["HS256"])
        except:
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        if not id.get('type') == 'access':
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        query = User.query.filter_by(id = id["id"]).first()
        password = query.password
        if not bcrypt.checkpw(self.params["password"].encode('utf-8'), password.encode('utf-8')):
            return Response(response=json.dumps({"error":"Bad Password"}), status=400, mimetype='application/json')
        query.password = bcrypt.hashpw(self.params["password1"].encode('utf-8') ,bcrypt.gensalt()).decode('utf-8')
        db.session.commit()
        return Response(response=json.dumps({}), status=200, mimetype='application/json')

class UpdateResult:
    def __init__(self, params, token):
        self.params = params
        self.token = token

    def execute(self):
        try:
            id = jwt.decode(self.token,settings.SECRET_KEY,algorithms=["HS256"])
        except:
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        if not id.get('type') == 'access':
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        query = User.query.filter_by(id = id["id"]).first()
        query.name = self.params["name"]
        query.last_name = self.params["lastname"]
        query.role = self.params["role"]
        db.session.commit()
        return Response(response=json.dumps({}), status=200, mimetype='application/json')

class UserResult:
    def __init__(self, token):
        self.token = token

    def execute(self):
        try:
            id = jwt.decode(self.token,settings.SECRET_KEY,algorithms=["HS256"])
        except:
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        if not id.get('type') == 'access':
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        query = User.query.filter_by(id = id["id"]).first()
        data = {
            'name': query.name,
            'last_name': query.last_name,
            'role': query.role,
            'email': query.email,
        }
        return Response(response=json.dumps(data), status=200, mimetype='application/json')