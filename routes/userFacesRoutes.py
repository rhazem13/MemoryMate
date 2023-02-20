from flask import request, Blueprint
from flask_restful import abort
from repositories.userFacesRepository import UserfacesRepository
from middlewares.validation.userFacesValidation import UserFacesSchema
from middlewares.auth import token_required

user_face_bp = Blueprint('userface', __name__)
manySchema=UserFacesSchema(many=True)
singleSchema=UserFacesSchema()
facesRepository= UserfacesRepository()
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

""" def post():
    errors= singleSchema.validate(request.form)
    if errors:
        return errors, 422
    

    payload =FacesSchema().load(request.form)
    print("found")

    if('id' in payload):
        return "Id field shouldn't be entered",422
    
    if 'user_face' not in request.files:
        resp=jsonify({'message' : 'No  image  in the request'})
        resp.status_code=400
        return resp
    user_face = request.files['user_face']
    if user_face.filename=='':
        resp=jsonify({'message' : 'No image selected for uploading'})
        resp.status_code=400
        return resp
    if user_face and allowed_file(user_face.filename):
         
     user_face_name = secure_filename(user_face.filename)
     user_face_path =  "static/faces/" + user_face_name
     user_face.save(user_face_path)

     payload['']=user_face_path #######add column name here
     resp=jsonify({'message' : 'face uploaded suecessfully'})
     resp.status_code=201
     return singleSchema.dump(faceRepository.create(payload))

    else:
     resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
     resp.status_code=400
     return resp """

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