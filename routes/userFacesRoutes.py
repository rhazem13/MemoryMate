from flask import jsonify, request, Blueprint
from flask_restful import abort
from repositories.userFacesRepository import UserfacesRepository
from middlewares.validation.userFacesValidation import UserFacesSchema
from middlewares.auth import token_required
from routes.userRoutes import allowed_file
from werkzeug.utils import secure_filename
import os
user_face_bp = Blueprint('userface', __name__)
manySchema=UserFacesSchema(many=True)
singleSchema=UserFacesSchema()
facesRepository= UserfacesRepository()
@user_face_bp.post('')
@token_required
def post():
    
    user_id = request.current_user.id
    errors= singleSchema.validate(request.form)
   
    if errors:
        print("moamewn")
        return errors, 422
    payload =UserFacesSchema().load(request.form)

    if('id' in payload):
        return "Id field shouldn't be entered",422
    
    
    # if('user_id' not in payload):
    #     return "user_id should be entered",422
    
    
    if 'file' not in request.files:
        resp = jsonify({'message':'No file part in the request'})
        resp.status_code=400
        return resp

    pic =request.files['file']

    if pic.filename=='':
        resp=jsonify({'message' : 'No image selected for uploading'})
        resp.status_code=400
        return resp
  
    os.mkdir(f'static/faces/{user_id}')

    if pic and allowed_file(pic.filename):
         user_face_name = secure_filename(pic.filename)
         img_path =  f"static/faces/{user_id}/" + user_face_name
         img_dic = "static/faces/Images/" + user_face_name
         pic.save(img_path)
         pic.save(img_dic)

         payload['face_url']=img_path 

         payload['user_id'] = user_id
         resp=jsonify({'message' : 'face uploaded suecessfully'})
         resp.status_code=201
    # return singleSchema.dump(faceRepository.create(payload))
    ##  img_path =  "MachineLearning/Face_Recognation/train/" + pic.filename
        
    # pic.save(img_path)    
         return singleSchema.dump(facesRepository.create(payload))
    else:
     resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
     resp.status_code=400
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