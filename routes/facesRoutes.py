from flask import request, Blueprint
from flask_restful import abort
from repositories.facesRepository import FacesRepository
from middlewares.validation.facesValidation import FacesSchema
face_bp = Blueprint('faces', __name__)
manySchema=FacesSchema(many=True)
singleSchema=FacesSchema()
faceRepository= FacesRepository()
@face_bp.post('')
def post():
    errors= singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    payload =FacesSchema().load(request.json)
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(faceRepository.create(payload))

@face_bp.get('')
def get():
    result= faceRepository.get_all()
    return manySchema.dump(result)

@face_bp.patch('/<int:id>')
def patch(id):
    errors= singleSchema.validate(request.get_json(),partial=True)
    if errors:
        return errors, 422
    payload =FacesSchema().load(request.get_json(),partial=True)
    result=faceRepository.update(payload,id)
    if not result:
        return "Location Id doesn't exist",404
    return singleSchema.dump(result)

@face_bp.delete('/<int:id>')
def delete(id):
    result = faceRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)