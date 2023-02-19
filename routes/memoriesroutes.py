from flask import request, Blueprint,jsonify
from flask_restful import abort
import os
from werkzeug.utils import secure_filename
from repositories.memoRepository import MemoryRepository
from middlewares.validation.userMemoryValidation import MemorySchema
from middlewares.auth import token_required

user_memories_bp = Blueprint('memory_picture', __name__)
memoryRepository = MemoryRepository()
memoryschema = MemorySchema()
UPLOAD_FOLDER = 'static\\memories\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_memories_bp.post('/memoadd')
@token_required
def post():
    errors= MemorySchema().validate(request.form)
    if errors:
        return errors, 422
    payload =MemorySchema().load(request.form)
 
    if 'thumbnail' not in request.files:
        resp=jsonify({'message' : 'No thumbnail image  in the request'})
        resp.status_code=400
        return resp
    thumbnail = request.files['thumbnail']
    if thumbnail.filename=='':
        resp=jsonify({'message' : 'No image selected for uploading'})
        resp.status_code=400
        return resp
    if thumbnail and allowed_file(thumbnail.filename):
         
     thumbnail_name = secure_filename(thumbnail.filename)
     thumbnail_path =  UPLOAD_FOLDER+ thumbnail_name
     thumbnail.save( thumbnail_path)

     payload['thumbnail']=thumbnail_path
     memoryRepository.create(payload)
     return MemorySchema().dump(memoryRepository.create(payload))
    else:
     resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
     resp.status_code=400
     return resp
     


