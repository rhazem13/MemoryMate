from flask import request, Blueprint
from flask_restful import abort
from repositories.userFacesRepository import UserfacesRepository
from middlewares.validation.userFacesValidation import UserFacesSchema
from middlewares.auth import token_required
from services.photoservice.photoservice import PhotoService

photoService = PhotoService.getInstance()
user_face_bp = Blueprint('userface', __name__)
manySchema=UserFacesSchema(many=True)
singleSchema=UserFacesSchema()
facesRepository= UserfacesRepository()

# testing the photo upload service
@user_face_bp.post('/test')
def postz():
    payload =request.json
    
    return {"result": photoService.addPhoto(payload['photo'],payload['folder'])}

@user_face_bp.get('/test/<int:id>')
def getz(id):
    photoService.addPhoto()
    return {"result": photoService.getPhoto(id)}

#######################################


@user_face_bp.post('')
@token_required
def post():
    
    errors= singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    payload =UserFacesSchema().load(request.json)
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(facesRepository.create(payload))

@user_face_bp.get('')
@token_required
def get():
    result= facesRepository.get_all()
    return manySchema.dump(result)

@user_face_bp.patch('/<int:id>')
@token_required
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
@token_required
def delete(id):
    result = facesRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)