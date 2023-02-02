from flask import request, Blueprint
from flask_restful import abort
from repositories.notificationsRepository import NotificationsRepository
from middlewares.validation.notificationsValidation import NotificationSchema
notification_bp = Blueprint('notification', __name__)
manySchema=NotificationSchema(many=True)
singleSchema=NotificationSchema()
notificationRepository= NotificationsRepository()
@notification_bp.post('')
def post():
    
    errors= singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    payload =NotificationSchema().load(request.json)
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(notificationRepository.create(payload))

@notification_bp.get('')
def get():
    result= notificationRepository.get_all()
    return manySchema.dump(result)

@notification_bp.patch('/<int:id>')
def patch(id):
    errors= singleSchema.validate(request.get_json(),partial=True)
    if errors:
        return errors, 422
    payload =NotificationSchema().load(request.get_json(),partial=True)
    result=notificationRepository.update(payload,id)
    if not result:
        return "Location Id doesn't exist",404
    return singleSchema.dump(result)

@notification_bp.delete('/<int:id>')
def delete(id):
    result = notificationRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)