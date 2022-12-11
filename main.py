from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request,jsonify,make_response,session
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
app.config['SECRET_KEY']='secret string'
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
def token_required(func):
    #//check and see if the token sent with the request ..if it's get it and make sure the token is valid
        @wraps(func) 
        def decorated(*args,**kwargs):
            token=request/args.get('token')
            if not token:
                return jsonify ({'Alert!':'token is missing'})
            try:
             payload=jwt.decode(token,app.config['SECRET_KEY'])
            except:
                return jsonify ({'Alert!':'invalid token'})


    
socketio.run(app, debug = True)

@app.route('/unprotected')
def unprotected():
    return ''

@app.route('/protected')
def protected():
    return ''
@app.roUte('/login')
def login():
    auth=request.authorization
# //get user and password sent along with the request
    if auth and auth.password =='password':

        token=jwt.encode({'user':auth.username,'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})
#//user:identify who the user is,exp:reserved part of payload tells the exprition date of the token

#/decorter:check to see if the token is along in the request if it is 
    return make_response ('couldnt verify!',401,{'WWW.Authenticate':'Basic realm="Login Requried"'})
    


