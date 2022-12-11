from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from flask_restful import Api
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
from models.db import db
from models.notificationModel import NotificationModel
from models.userAgendaModel import UserAgenda
from models.userLocationsModel import UserLocationModel
from routes.userRoutes import UserRouter
from flask_migrate import Migrate
load_dotenv()

app = Flask(__name__)
api = Api(app)
# print (os.getenv('DB_URL'))
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = 'secret string'
migrate= Migrate(app,db)
migrate.init_app(app, db)

api.add_resource(UserRouter,'/')
socketio  = SocketIO(app, cors_allowed_origins='*')
db.init_app(app)
@socketio.on('connect')
def test_connect():
    print('sharaf')
    socketio.emit('after connect', {'data':'Let us learn Web Socket in Flask'})
# with app.app_context():
#     db.create_all()

#if __name__ == "main":
#app.run(debug = True)
socketio.run(app, debug = True)
