from flask import request, Blueprint,jsonify
from flask_restful import abort
from models.db import db
import os
from werkzeug.utils import secure_filename
from repositories.memoRepository import MemoryRepository
from models.Memories.userMemoriesModel import MemoryModel
from middlewares.validation.userMemoryValidation import MemorySchema
from repositories.userRepository import UserRepository
from repositories.caregiverMemoRepository import caregiverMemoryRepository 

from middlewares.auth import token_required
from sqlalchemy import exc
from services.photoservice.photoservice import PhotoService


photoService = PhotoService.getInstance()
user_memories_bp = Blueprint('memory', __name__)
memoryRepository = MemoryRepository()
memoryschema = MemorySchema()
memoryManyschema = MemorySchema(many=True)
Folder_Name="memory thumbnail"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_memories_bp.post('/memoadd')
@token_required
def post():
    current_user = request.current_user
    errors= MemorySchema().validate(request.json)
    
    if errors:
        return errors, 422
    payload =MemorySchema().load(request.json)
    if not current_user.id==payload['user_id']:
        return jsonify({'message' : 'not a valid user'},403)
    
    # if 'thumbnail' not in request.files:
    #     resp=jsonify({'message' : 'No thumbnail image  in the request'})
    #     resp.status_code=400
    #     return resp
    # thumbnail = request.files['thumbnail']
    # if thumbnail.filename=='':
    #     resp=jsonify({'message' : 'No image selected for uploading'})
    #     resp.status_code=400
    #     return resp
    # if thumbnail and allowed_file(thumbnail.filename):
         
    #  thumbnail_name = secure_filename(thumbnail.filename)
    #  thumbnail_path =  UPLOAD_FOLDER+ thumbnail_name
    #  thumbnail.save( thumbnail_path)

    #  payload['thumbnail']=thumbnail_path
    photo_url=photoService.addPhoto(payload['thumbnail'],Folder_Name)
    payload['thumbnail']=photo_url
    memory=memoryRepository.create(payload)
    return MemorySchema().dump(memory)
    # else:
    #  resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
    #  resp.status_code=400
    #  return resp
    


@user_memories_bp.post('/caregiveradd/<memo_id>') #add caregivers 
@token_required
def addcaregiver(memo_id):
        payload =request.json
        memory=memoryRepository.get_by_id(memo_id)
        caregivers=[]
        try:
         caregivers_ids=payload['caregivers_ids']
         for caregiver_id in caregivers_ids:
             cg=UserRepository().get_by_id(caregiver_id)
             caregivers.append(cg)
         (memory.caregivers).extend(caregivers)
         resp = jsonify({'message' : 'caregivers added successfully'})
         resp.status_code=200
         db.session.commit()
         return resp
        except exc.SQLAlchemyError as err:
            print(type(err))
            return {'message' : 'failed to add caregivers'}


# @user_memories_bp.get('/memoesget') #get all memories
# @token_required
# def getmemos():
 
#      memos= memoryRepository.get_all()
#      return memoryManyschema.dump(memos)

@user_memories_bp.get('/usermemoget') #get memos of current user
@token_required
def geUsermemos():
    current_user = request.current_user
    USERmemos = MemoryModel.query.filter_by(user_id=current_user.id).all()
    if not USERmemos:
                return jsonify({'message' : 'No memory found!'})

    return memoryManyschema.dump(USERmemos)

@user_memories_bp.get('/memoget/<memo_id>') #get specific memo of current user
@token_required
def getmemo(memo_id):
    current_user = request.current_user
    memo = MemoryModel.query.filter_by(id=memo_id, user_id=current_user.id).first()
    if not memo:

         return {'message' : ' memory  not found for the current user!'}

    return memoryschema.dump(memo)

@user_memories_bp.get('/userget') #####get user info from memory
@token_required
def getuser():
    current_user = request.current_user

    memo = MemoryModel.query.filter_by( user_id=current_user.id).first()
    usr=memo.patient.photo_path

    return {"user photo is":usr}


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
        return "memory can't be updated",404
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
        return jsonify({"the following memory id is deleted" :f"{memo.id}"}),404

@user_memories_bp.delete('/deletecaregiver/<memo_id>') #delete caregivers 
@token_required
def deletecaregiver(memo_id):
        payload =request.json
        try:
         caregivers_ids=payload['caregivers_ids']
         for caregiver_id in caregivers_ids:
            caregiverMemoryRepository().delete(memo_id,caregiver_id)
         resp = jsonify({'message' : 'caregivers deleted successfully'})
         resp.status_code=200
         return resp
        except exc.SQLAlchemyError as err:
            print(type(err))
            return jsonify({'message' : 'failed to delete caregivers'},403)