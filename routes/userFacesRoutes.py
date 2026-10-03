from utils.images import save_face
from utils.images import face_directory
from pathlib import Path
from flask import jsonify, request, Blueprint, send_file
from flask_restful import abort
from models.UserFaces.userfacesModel import UserfacesModel
from repositories.userFacesRepository import UserfacesRepository
from middlewares.validation.userFacesValidation import UserFacesSchema
from middlewares.auth import token_required
from werkzeug.utils import secure_filename
import os
import base64
from PIL import Image
from io import BytesIO
from services.photoservice.photoservice import PhotoService

photoService = PhotoService.getInstance()
user_face_bp = Blueprint('userface', __name__)
manySchema=UserFacesSchema(many=True)
singleSchema=UserFacesSchema()
facesRepository= UserfacesRepository()

@user_face_bp.post('')
@token_required
def post():
    
    user_id = request.current_user.id
    name = request.json['name']
    bio = request.json['bio']
    errors= singleSchema.validate(request.json)
   
    if errors:
        return errors, 422
    payload =UserFacesSchema().load(request.json)

    if('id' in payload):
        return "Id field shouldn't be entered",422
    
    
    
    if 'face_url' not in request.json:
        resp = jsonify({'message':'No file part in the request'})
        resp.status_code=400
        return resp

    payload['face_url'] = save_face(request.json['face_url'])

    payload['user_id'] = user_id

    payload['name'] = name
    payload['bio'] = bio


    resp=jsonify({'message' : 'face uploaded suecessfully'})
    resp.status_code=201

    singleSchema.dump(facesRepository.create(payload))

    return resp

    


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
    if facesRepository.get_by_id(id) is None:
        abort(404)
    if 'face_url' in payload:
        payload['face_url'] = save_face(payload['face_url'])
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


@user_face_bp.get('/<int:id>/image')
@token_required
def image(id):
    face = facesRepository.get_by_id(id)
    if face is None:
        abort(404)
    path = (face_directory() / face.face_url).resolve()
    if not path.is_relative_to(face_directory().resolve()) or not path.is_file():
        abort(404)
    return send_file(path)
