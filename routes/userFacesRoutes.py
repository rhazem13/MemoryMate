from flask import request, Blueprint
from flask_restful import abort
from repositories.userFacesRepository import UserfacesRepository
from middlewares.validation.userFacesValidation import UserFacesSchema
user_face_bp = Blueprint('userface', __name__)
manySchema=UserFacesSchema(many=True)
singleSchema=UserFacesSchema()
facesRepository= UserfacesRepository()
@user_face_bp.post('')
def post():
    
    errors= singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    payload =UserFacesSchema().load(request.json)
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(facesRepository.create(payload))

@user_face_bp.get('')
def get():
    result= facesRepository.get_all()
    return manySchema.dump(result)

@user_face_bp.patch('/<int:id>')
def patch(id):
    errors= singleSchema.validate(request.get_json(),partial=True)
    if errors:
        return errors, 422
    payload =UserFacesSchema().load(request.get_json(),partial=True)
    result=facesRepository.update(payload,id)
    if not result:
        return "Location Id doesn't exist",404
    return singleSchema.dump(result)

@user_face_bp.delete('/<int:id>')
def delete(id):
    result = facesRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)