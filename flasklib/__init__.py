from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dgquatlcvznxnr:3a6392d56bfbb9091ab8a8b08fb0a78ea67f17b7de2f54f48668f8663cc30daf@ec2-63-32-173-118.eu-west-1.compute.amazonaws.com:5432/d4cl3hr6h2gpdq'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from flasklib import routes