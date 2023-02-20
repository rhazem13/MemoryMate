from flask import request, Blueprint,jsonify
from flask_restful import abort
import os
from werkzeug.utils import secure_filename
from repositories.memoRepository import MemoryRepository
from models.Memories.userMemoriesModel import MemoryModel
from middlewares.validation.userMemoryValidation import MemorySchema
from repositories.userRepository import UserRepository
from middlewares.auth import token_required

user_memories_bp = Blueprint('memory', __name__)
memoryRepository = MemoryRepository()
memoryschema = MemorySchema()
memoryManyschema = MemorySchema(many=True)
UPLOAD_FOLDER = 'static\\memories\\'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_memories_bp.post('/memoadd')
@token_required
def post():
    current_user = request.current_user
    errors= MemorySchema().validate(request.form)
    if errors:
        return errors, 422
    payload =MemorySchema().load(request.form)
    if not current_user.id==payload['user_id']:
        return {'message' : 'not a valid user'}
    
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

@user_memories_bp.get('/memoesget')
@token_required
def getmemos():
 
     memos= memoryRepository.get_all()
     return memoryManyschema.dump(memos)

@user_memories_bp.get('/usermemoget') #get memo of specific user
@token_required
def geUsermemos():
    current_user = request.current_user
    USERmemos = MemoryModel.query.filter_by(user_id=current_user.id).all()
    if not USERmemos:
                return jsonify({'message' : 'No memory found!'})

    return memoryManyschema.dump(USERmemos)

@user_memories_bp.get('/memoget/<memo_id>') #get memo of specific user
@token_required
def getmemo(memo_id):
    current_user = request.current_user
    memo = MemoryModel.query.filter_by(id=memo_id, user_id=current_user.id).first()
    if not memo:

         return {'message' : ' memory  not found for the current user!'}

    return memoryschema.dump(memo)


@user_memories_bp.patch('memopatch/<memo_id>')
@token_required
def patch(memo_id):
    current_user = request.current_user
    errors= memoryschema.validate(request.form,partial=True)
    if errors:
        return errors, 422
    memo = MemoryModel.query.filter_by(id=memo_id, user_id=current_user.id).first()
    if not memo:

         return {'message' : ' memory  not found for the current user!'}
    payload = MemorySchema().load(request.form,partial=True)
    result=memoryRepository.update(payload,memo_id)
    if not result:
        return "memory Id doesn't exist",404
    return memoryschema.dump(result)

@user_memories_bp.delete('/memodel/<memo_id>')
@token_required
def delete(memo_id):
    current_user = request.current_user
    memo = MemoryModel.query.filter_by(id=memo_id, user_id=current_user.id).first()
    if not memo:
        return {'message' : ' memory not found for the current user!'}
    result = memoryRepository.delete(memo.id)
    if(result):
        return {"the following memory id is deleted" :f"{memo.id}"}
    abort(404)



