from flask import request, Blueprint,jsonify
from flask_restful import abort
from repositories.facesRepository import FacesRepository
from middlewares.validation.facesValidation import FacesSchema
from werkzeug.utils import secure_filename

from middlewares.auth import token_required

face_bp = Blueprint('faces', __name__)
manySchema=FacesSchema(many=True)
singleSchema=FacesSchema()
faceRepository= FacesRepository()
UPLOAD_FOLDER = 'static\\faces\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@face_bp.post('/faceadd')
@token_required
def post():
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
     return resp

@face_bp.get('')
@token_required
def get():
    result= faceRepository.get_all()
    return manySchema.dump(result)

@face_bp.patch('/<int:id>')
@token_required
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
@token_required
def delete(id):
    result = faceRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)