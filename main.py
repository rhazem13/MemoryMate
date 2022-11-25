from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from models.db import db
from flask_restful import Api
from models.db import db

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://rhazem13:Hazm1102001@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = 'secret string'

db.init_app(app)
with app.app_context():
    db.create_all()

