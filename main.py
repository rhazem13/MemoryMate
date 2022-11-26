from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request 
from flask_restful import Api
from flask_socketio import SocketIO
from models.db import db
from routes.userRoutes import UserRouter
from models.notificationModel import NotificationModel
from models.userAgendaModel import UserAgenda
from models.userLocationsModel import UserLocationModel
from routes.userRoutes import UserRouter
from flask_migrate import Migrate
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Hazm1102001@localhost/testone'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
migrate= Migrate(app,db)
app.secret_key = 'secret string'
api.add_resource(UserRouter,'/')
socketio  = SocketIO(app, cors_allowed_origins='*')
# db.init_app(app)
# migrate = Migrate()
@socketio.on('connect')
def test_connect():
    print('sharaf')
    socketio.emit('after connect', {'data':'Let us learn Web Socket in Flask'})
with app.app_context():
    db.create_all()

#if __name__ == "main":
#app.run(debug = True)
socketio.run(app, debug = True)
