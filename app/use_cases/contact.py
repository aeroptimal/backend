from flask import Response, render_template, current_app
from flask_mail import Mail, Message
import json

from conf import settings

class ContactResponse:
    def __init__(self, params):
        self.params = params

    def execute(self):
        name = self.params.get('name')
        email = self.params.get('email')
        request = self.params.get('request')
        mail = Mail()
        msg = Message('Contact',
                        sender=("AeroOptimal",settings.EMAIL_USER),
                        recipients = ["aeroptimal@hotmail.com"], 
                        )
        msg.html = render_template('email.html',host=settings.DOMAIN,title=f"Email from {name}",content=f"{request}\n\n{email}")
        mail.send(msg)
        return Response(response=json.dumps({}), status=201, mimetype='application/json')