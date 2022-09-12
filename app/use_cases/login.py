from models.model import User, db
from conf import settings

import json
import jwt
import bcrypt
from flask import Response, render_template, current_app
from flask_mail import Mail, Message
from secrets import token_hex
import datetime

class Activate:
    def __init__(self, token):
        self.token = token

    def execute(self):
        try:
            id = jwt.decode(self.token,settings.SECRET_KEY,algorithms=["HS256"])
        except:
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        if not id.get('type') == 'activate':
            return Response(response=json.dumps({"error":"Bad login"}), status=400, mimetype='application/json')
        query = User.query.filter_by(id = id["id"]).first()
        query.active = True
        db.session.commit()
        return Response(response=json.dumps({}), status=200, mimetype='application/json')

class LoginResult:
    def __init__(self, params):
        self.params = params

    def execute(self):
        query = User.query.filter_by(email=self.params.get('email').lower().replace(' ','')).first()
        if query:
            hashed = query.password.encode('utf-8')
            password = self.params.get('password').encode('utf-8')
            if bcrypt.checkpw(password, hashed):
                active = query.active
                if not active:
                    return Response(response=json.dumps({"error":"User not active"}), status=400, mimetype='application/json')
                id = query.id
                name = query.name
                token = jwt.encode({"id":id,"type":"access","exp": datetime.datetime.now() + datetime.timedelta(days=1)},settings.SECRET_KEY,algorithm="HS256")
                return Response(json.dumps({'token': token, "name": name}), status=201, mimetype='application/json')
            return Response(response=json.dumps({"error":"Invalid password"}), status=400, mimetype='application/json')
        return Response(response=json.dumps({"error":"Email not registered"}), status=400, mimetype='application/json')

class SignupResult:
    def __init__(self, params):
        self.params = params

    def execute(self):
        if User.query.filter_by(email=self.params['email'].lower().replace(' ','')).first():
            return Response(response=json.dumps({"error":"User already exists"}), status=400, mimetype='application/json')
        id = token_hex(8) 
        hashed = bcrypt.hashpw(self.params.get('password').encode('utf8'), bcrypt.gensalt()).decode('utf8')
        user = User(
            id=id,
            name=self.params.get('name'),
            last_name=self.params.get('lastname'),
            email=self.params.get('email').lower().replace(' ',''),
            password=hashed,
            role=self.params.get('role')
        )
        db.session.add(user)
        db.session.commit()
        token = jwt.encode({"id":id,"type":"activate","exp": datetime.datetime.now() + datetime.timedelta(minutes=15)},settings.SECRET_KEY,algorithm="HS256")
        with current_app.app_context():
            mail = Mail()
            msg = Message('Activation Request',
                            sender=("AeroOptimal",settings.EMAIL_USER),
                            recipients = [self.params.get('email').lower().replace(' ','')], 
                            )
            msg.html = render_template('email.html',title=f"Hello {self.params.get('name')}",content=f"Activate your account here:",a_name="Activate",a=f"{settings.DOMAIN}/activate?id={token}")
            mail.send(msg)
        return Response(json.dumps({}), status=200, mimetype='application/json')
