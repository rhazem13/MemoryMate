from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, make_response, session
from flask_restful import Api
from flask_socketio import SocketIO
from flask_migrate import Migrate
from services.caching.caching import CacheService
from dotenv import load_dotenv
from models.db import db
from routes.userRoutes import user_bp
from routes.userLocationRoutes import user_location_bp
from routes.userAgendaRoutes import user_agenda_bp
from routes.userCalendarRoutes import user_calendar_bp
from routes.facesRoutes import face_bp
from routes.notificationRoutes import notification_bp
from routes.userContactsRoutes import user_contacts_bp
from routes.userFacesRoutes import user_face_bp
from routes.eventsRoutes import events_bp
from repositories.notificationsRepository import NotificationsRepository
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from services.EventEmitter.event_emitter import EventEmitter
from repositories.userAgendaRepository import UserAgendaRepository
from services.redis.redis import RedisService
from middlewares.auth import token_required
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler


#from routes.AlzhemerRoutes import ALZhemer
#from routes.FaceRecognationRoutes import FaceRecognation
load_dotenv()

app = Flask(__name__)
api = Api(app)
# Set the configuration variables to the flask application
app.config.from_object('config.Config')

migrate = Migrate(app, db)
migrate.init_app(app, db)
ma = Marshmallow(app)
db.init_app(app)
redis_client = RedisService.getClient(app)
CacheService.initialize(app)
app.register_blueprint(user_bp, url_prefix='/users')
app.register_blueprint(user_location_bp, url_prefix='/userlocation')
app.register_blueprint(user_agenda_bp, url_prefix='/useragenda')
app.register_blueprint(user_calendar_bp, url_prefix='/usercalendar')
app.register_blueprint(face_bp, url_prefix='/faces')
app.register_blueprint(notification_bp, url_prefix='/notifications')
app.register_blueprint(user_contacts_bp, url_prefix='/usercontacts')
app.register_blueprint(user_face_bp, url_prefix='/userfaces')
app.register_blueprint(events_bp, url_prefix='/events')
#app.register_blueprint(ALZhemer, url_prefix='/Alzahemer')
#app.register_blueprint(FaceRecognation, url_prefix='/Face')

socketio = SocketIO(app, cors_allowed_origins='*')
emitter = EventEmitter.getInstance()


def notify_patients_drugs():
    with app.app_context():
        print('time scheduler ')
        print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
        agendas = UserAgendaRepository.findWithenInterval(5)
        for agenda in agendas:
            print(agenda)
            id = agenda.id
            redis_client.set(f"agenda-{id}", "False")
            user_id = agenda.user_id
            notification = {
                "user_id": user_id,
                "title": "لقد نسيت أخذ الدواء",
                "body": {
                    "content": "لقد نسيت اخذ دواء الساعة 7"
                },
                "type": "important"
            }
            print(emitter._callbacks)
            emitter.emit(f"notify_user-{user_id}", user_id,  notification)

        UserAgendaRepository.updateStartTimeWithInterval()
        expired_agendas = UserAgendaRepository.getExpiredAgenda()
        for agenda in expired_agendas:
            emitter.emit(f"notify_user-{user_id}", user_id, {
                "user_id": user_id,
                "title": "قريبك مخدش الدوا",
                "body": {
                    "content": "قريبك نسي ياخد الدوا"
                },
                "type": "important"
            })


scheduler = BackgroundScheduler()
scheduler.add_job(func=notify_patients_drugs, trigger="interval", seconds=60)
""" scheduler.start()
atexit.register(lambda: scheduler.shutdown())
 """

def notify_user(user_id, notification):
    print('notification for user ', user_id, notification)
    NotificationsRepository().create(notification)
    socketio.emit('agenda-notify', {"content": "hiiiiiii"})
    print('emit for user')


@socketio.on('connect')
@token_required
def test_connect(cur_user):
    user_id = cur_user.id
    emitter.on(f'notify_user-{user_id}', notify_user)
    socketio.emit('after connect', {
                  'data': 'Let us learn Web Socket in Flask'})


@socketio.on('reminded')
@token_required
def agenda_reminded(cur_user, data):
    agenda_id = data['agenda_id']
    redis_client.delete(f"agenda-{agenda_id}")

# testing emitter,, hazem


def update_location():
    print("send new location ")


emitter.on('update-location', update_location())
################################
# with app.app_context():
#     db.create_all()


app.run(debug=True)
print('starting socket')
#socketio.run(app, debug = True, host='127.0.0.1')
