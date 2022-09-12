from flask_sqlalchemy import SQLAlchemy
import datetime


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(16), unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    payment_status = db.Column(db.Boolean, nullable=False, default=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return '<User %s>' % self.id

class Articles(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    date = db.Column(db.Date, nullable=False)
    link = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Articles %s>' % self.title

class News(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return '<News %s>' % self.title
