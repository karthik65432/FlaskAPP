from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SECRET_KEY'] = '9886144146'
db = SQLAlchemy(app)


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime(), nullable=False, default=datetime.now(pytz.timezone('Asia/Kolkata')))

    def __repr__(self):
        return 'Blog post ' + str(self.id)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default= 'default.jpg')
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.now(pytz.timezone('Asia/Kolkata')))

    def __repr__(self):
        return f'{self.username} : {self.email} : {self.date_created}'