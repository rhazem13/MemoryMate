from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request,jsonify,make_response,session
from flask_restful import Api
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_caching import Cache
from services.caching.caching import CacheService
import os
from dotenv import load_dotenv
from models.db import db
from routes.userRoutes import user_bp
from routes.userLocationRoutes import user_location_bp
from routes.userAgendaRoutes import user_agenda_bp
from routes.userCalendarRoutes import user_calendar_bp
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config.from_object('config.Config')  # Set the configuration variables to the flask application

migrate= Migrate(app,db)
migrate.init_app(app, db)
ma = Marshmallow(app)
db.init_app(app)
CacheService.initialize(app)
from routes.userRoutes import UserRouters
userRouter =  UserRouters()
app.register_blueprint(userRouter.user_bp, url_prefix='/users')
app.register_blueprint(user_location_bp, url_prefix='/userlocation')
app.register_blueprint(user_agenda_bp, url_prefix='/useragenda')
app.register_blueprint(user_calendar_bp, url_prefix='/usercalendar')
socketio  = SocketIO(app, cors_allowed_origins='*')

@socketio.on('connect')
def test_connect():
    print('sharaf')
    socketio.emit('after connect', {'data':'Let us learn Web Socket in Flask'})

# with app.app_context():
#     db.create_all()

if __name__ == "main":

    #app.run(debug = True)
    print('starting socket')
    socketio.run(app, debug = True, host='127.0.0.1')

