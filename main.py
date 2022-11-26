from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from flask_restful import Api
from models.db import db
from models.userModel import UserModel
from models.notificationModel import NotificationModel
from models.userAgendaModel import UserAgenda
from models.userLocationsModel import UserLocationModel

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hazm1102001@localhost/testone'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = 'secret string'

db.init_app(app)
with app.app_context():
    db.create_all()
    print('creating all tables')
    


if __name__ == "__main__":
    app.run(debug=True)