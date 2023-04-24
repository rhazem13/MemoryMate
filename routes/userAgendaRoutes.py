from datetime import timedelta
from flask import request, Blueprint
from flask_restful import abort
from repositories.agendaRepository import AgendaRepository
from middlewares.validation.userAgendaValidation import UserAgendaSchema
from middlewares.auth import token_required

from middlewares.auth import token_required
user_agenda_bp = Blueprint('useragenda', __name__)
manySchema=UserAgendaSchema(many=True)
singleSchema=UserAgendaSchema()
agendaRepository = AgendaRepository()
@user_agenda_bp.post('')
@token_required
def post():
    errors= UserAgendaSchema().validate(request.get_json())
    if errors:
        return errors, 422
    payload =UserAgendaSchema().load(request.json)
    payload['user_id']=request.current_user.id
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(agendaRepository.create(payload))

@user_agenda_bp.get('')
@token_required
def get():
    result= agendaRepository.get_all()
    return manySchema.dump(result)

@user_agenda_bp.patch('/<int:id>')
@token_required
def patch(id):
    errors= UserAgendaSchema().validate(request.get_json(),partial=True)
    if errors:
        return errors, 422
    payload =UserAgendaSchema().load(request.json,partial=True)
    result = agendaRepository.update(payload,id)
    if not result:
        return "agenda id not found",404
    return singleSchema.dump(result)

@user_agenda_bp.delete('/<int:id>')
@token_required
def delete(id):
    result = agendaRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)