from flask import Flask, request, jsonify, make_response, session
from flask_restful import Api
from flask_migrate import Migrate
from services.caching.caching import CacheService
from dotenv import load_dotenv
from models.db import db
from middlewares.SocketAuth import *
from routes.userRoutes import user_bp
from routes.userLocationRoutes import user_location_bp
from routes.memoriesroutes import user_memories_bp
from routes.memoPicturesRoutes import memories_pics_bp
from routes.userAgendaRoutes import user_agenda_bp
from routes.userCalendarRoutes import user_calendar_bp
from routes.notificationRoutes import notification_bp
from flask_cors import CORS
from routes.userContactsRoutes import user_contacts_bp
from routes.userFacesRoutes import user_face_bp
from routes.eventsRoutes import events_bp
from repositories.userRepository import UserRepository
from routes.caringRoutes import caring_bp
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from services.EventEmitter.event_emitter import EventEmitter
from routes.AlzhemerRoutes import ALZhemer
from routes.FaceRecognationRoutes import FaceRecognation
from repositories.userAgendaRepository import UserAgendaRepository
from services.redis.redis import RedisService
from services.socket.socket import SocketService
from middlewares.auth import token_required
from events.agenda.CaregiverAgendaEvent import CaregiverAgendaEvent
from events.agenda.PatientAgendaEvent import PatientAgendaEvent
import time
import atexit
import pickle
from apscheduler.schedulers.background import BackgroundScheduler
load_dotenv()
app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

api = Api(app)
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
# app.register_blueprint(face_bp, url_prefix='/faces')
app.register_blueprint(notification_bp, url_prefix='/notifications')
app.register_blueprint(user_contacts_bp, url_prefix='/usercontacts')
app.register_blueprint(user_memories_bp, url_prefix='/memories')
app.register_blueprint(memories_pics_bp, url_prefix='/memopics')
app.register_blueprint(user_face_bp, url_prefix='/userfaces')
app.register_blueprint(events_bp, url_prefix='/events')
app.register_blueprint(caring_bp, url_prefix='/caring')
app.register_blueprint(ALZhemer, url_prefix='/Alzahemer')
app.register_blueprint(FaceRecognation, url_prefix='/Face')


emitter = EventEmitter.getInstance()

# def notify_patients_drugs():
#     with app.app_context():
#         print('time scheduler ')
#         print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
#         agendas = UserAgendaRepository.findWithenInterval(5)
#         for agenda in agendas:
#             id = agenda.id
#             if redis_client.get(f"agenda-{id}"):
#                 continue
#             redis_client.set(f"agenda-{id}", "False")
#             user_id = agenda.user_id
#             PatientAgendaEvent().notify(None, user_id,
#                                         f"notify_user-{user_id}", {"agenda_id": agenda.id, "room": redis_client.get(user_id)})
#         expired_agendas = UserAgendaRepository.getExpiredAgenda()
#         UserAgendaRepository.updateStartTimeWithInterval()
#         for agenda in expired_agendas:
#             agenda_id = agenda.id
#             if redis_client.get(f"agenda-{agenda_id}") is None:
#                 continue
#             caregivers = UserRepository.get_caregivers_by_patient_id(agenda.user_id)
#             for caregiver in caregivers:
#                 caregiver_id = caregiver.id
#                 CaregiverAgendaEvent().notify(None, caregiver_id, f"notify_user-{caregiver_id}", {
#                     "agenda_id": agenda.id, "room": redis_client.get(user_id)})
#                 redis_client.delete(f"agenda-{agenda_id}")
#         UserAgendaRepository.updateStartTimeWithInterval()


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=notify_patients_drugs, trigger="interval", seconds=60)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    print('on main')
    socketio = SocketService.getSocket(app)

    @socketio.on('connect')
    @token_required
    def on_connect():
        cur_user = request.current_user
        user_id = cur_user.id
        redis_client.set(user_id, request.sid)
        print("user ", {cur_user}, " with id", user_id, "connected")

    @socketio.on('reminded')
    @token_required
    def agenda_reminded(data):
        agenda_id = data['agenda_id']
        redis_client.delete(f"agenda-{agenda_id}")
        UserAgendaRepository.updateAgendaStartTimeWithInterval(
            data['agenda_id'])
    app.run(host="0.0.0.0", debug=True, use_reloader=False)
print('starting socket')
#socketio.run(app, debug = True, host='127.0.0.1')
