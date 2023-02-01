from flask import request, Blueprint
from flask_restful import  abort
from repositories import calendarRepository
from middlewares.validation.userCalendarValidation import UserCalendarSchema
user_calendar_bp = Blueprint('usercalendar', __name__)
manySchema=UserCalendarSchema(many=True)
singleSchema=UserCalendarSchema()

@user_calendar_bp.post('')
def post():
    errors= UserCalendarSchema().validate(request.get_json())
    if errors:
        return errors, 422
    payload =UserCalendarSchema().load(request.json)
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(calendarRepository.create(payload))

@user_calendar_bp.get('')
def get():
    calendarList= calendarRepository.get_all()
    return manySchema.dump(calendarList)

@user_calendar_bp.patch('/<int:id>')
def patch(id):
    errors= UserCalendarSchema().validate(request.get_json(),partial=True)
    if errors:
        return errors, 422
    payload =UserCalendarSchema().load(request.json,partial=True)
    result = calendarRepository.update(payload,id)
    if not result:
        return "Calendar id not found",404
    return singleSchema.dump(result)

@user_calendar_bp.delete('/<int:id>')
def delete(id):
    result = calendarRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)