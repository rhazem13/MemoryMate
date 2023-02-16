from flask import request, Blueprint
from flask_restful import abort
from services.EventEmitter.event_emitter import EventEmitter
from repositories.notificationsRepository import NotificationsRepository
from models.Notifications.notificationsModel import NotificationsModel
from middlewares.validation.notificationsValidation import NotificationSchema
from middlewares.auth import token_required

notificationsRepository = NotificationsRepository()
events_bp = Blueprint('events', __name__)
emitter= EventEmitter.getInstance()

@events_bp.post('/updateCurrentLocation')
def post():
    payload =NotificationSchema().load(request.json)
    notificationsRepository.create(payload)
    emitter.emit("updateCurrentLocation")
    return "updated Current Location",200