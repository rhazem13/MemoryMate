from flask import jsonify, request, Blueprint
from flask_restful import abort
from models.UserFaces.userfacesModel import UserfacesModel
from repositories.userFacesRepository import UserfacesRepository
from middlewares.validation.userFacesValidation import UserFacesSchema
from middlewares.auth import token_required
from routes.userRoutes import allowed_file
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

# testing the photo upload service
@user_face_bp.post('/test')
def postz():
    result = request.json
    return {"result": photoService.addPhoto(result['photo'],result['folder'])}

@user_face_bp.get('/test/<int:id>')
def getz(id):
    photoService.addPhoto()
    return {"result": photoService.getPhoto(id)}

#######################################


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

    pic =request.json['face_url']
  


    starter = pic.find(',')
    image_data = pic[starter+1:]
    image_data = bytes(image_data, encoding="ascii")
    im = Image.open(BytesIO(base64.b64decode(image_data)))
        

    img_path =  f"static/faces/Images/{name}.jpg" 

    im.save(img_path)


    payload['face_url']=img_path 

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