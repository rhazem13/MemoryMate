from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request,jsonify,make_response,session
from flask_restful import Api
from flask_socketio import SocketIO
import os
from dotenv import load_dotenv
from models.db import db
from routes.userRoutes import user_bp
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


load_dotenv()

app = Flask(__name__)
api = Api(app)
app.config.from_object('config.Config')  # Set the configuration variables to the flask application
app.register_blueprint(user_bp, url_prefix='/users')
migrate= Migrate(app,db)
migrate.init_app(app, db)
ma = Marshmallow(app)

socketio  = SocketIO(app, cors_allowed_origins='*')
db.init_app(app)
@socketio.on('connect')
def test_connect():
    print('sharaf')
    socketio.emit('after connect', {'data':'Let us learn Web Socket in Flask'})

# with app.app_context():
#     db.create_all()

#if __name__ == "main":
app.run(debug = True)


    
#socketio.run(app, debug = True)

