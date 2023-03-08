from flask import request, Blueprint,jsonify
from flask_restful import abort
import os
from werkzeug.utils import secure_filename
from repositories.memoPicsRepository import MemoryPicsRepository
from middlewares.validation.memoPicsValiation import MemoryPicSchema
from repositories.userRepository import UserRepository
from middlewares.auth import token_required
from models.Memories.memoryPicsModel import MemoPictures
from models.Memories.userMemoriesModel import MemoryModel
from services.photoservice.photoservice import PhotoService


photoService = PhotoService.getInstance()
memories_pics_bp = Blueprint('memory_picture', __name__)
memory_pictures_Repository = MemoryPicsRepository()
memoryPicschema = MemoryPicSchema()
memoryPicManyschema = MemoryPicSchema(many=True)
Folder_Name="memories pictures"
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@memories_pics_bp.post('/memopicsadd') #add memo pic
@token_required
def post():
    current_user = request.current_user

    errors=  MemoryPicSchema().validate(request.json)
    if errors:
        return errors, 422
    
    payload = MemoryPicSchema().load(request.json)
    memopic=MemoryPicsRepository.get_by_memory_id(payload['memory_id'])
    if not  memopic:
         return {'message' : 'memory not found '}
    if not  memopic.user_id==current_user.id:
      return {'message' : 'not a valid memory for the current user'}
       
    # if 'memoPic_path' not in request.files:
    #     resp=jsonify({'message' : 'No  image  in the request'})
    #     resp.status_code=400
    #     return resp
    # memory_picture =payload['memoPic_path']
    # if memory_picture.filename=='':
    #     resp=jsonify({'message' : 'No image selected for uploading'})
    #     resp.status_code=400
    #     return resp
    # if memory_picture and allowed_file(memory_picture.filename):
         
    #  memory_picture_name = secure_filename(memory_picture.filename)
    #  memory_picture_path =  UPLOAD_FOLDER+ memory_picture_name
    #  memory_picture.save( memory_picture_path)

    #  payload['memoPic_path']=memory_picture_path
    
    photo_url=photoService.addPhoto(payload['memoPic_path'],Folder_Name)
    payload['memoPic_path']=photo_url
    return MemoryPicSchema().dump(memory_pictures_Repository.create(payload))
    # else:
    #  resp = jsonify({'message' : 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
    #  resp.status_code=400
    #  return resp


@memories_pics_bp.get('/memopicsget/<memo_id>') #get memo pics of specific memory
@token_required
def getmemospics(memo_id):
    current_user = request.current_user

    memopics = MemoPictures.query.filter_by(memory_id=memo_id).all()
    for memopic in memopics:
    
     if not memopic.memory.user_id==current_user.id:
       print(memopic.memory.user_id)
       return jsonify({'message' : 'No memory found!'})
    return memoryPicManyschema.dump(memopics)


@memories_pics_bp.get('/usermemopicsget') #get memo pics of specific user
@token_required
def usergetmemospics():
    current_user = request.current_user


    usermemopics=MemoryPicsRepository().get_all()
    if not usermemopics:
       {'message' : 'No memory found for the current user!'}

    userpics=[]
    for usermemopic in usermemopics:
     if  usermemopic.memory.user_id==current_user.id:
       userpics.append(usermemopic)
    return memoryPicManyschema.dump(userpics)

@memories_pics_bp.get('/memopicget/<memopic_id>') #get specific memo pic of specific user
@token_required
def getmemo(memopic_id):
    current_user = request.current_user

    memopic = MemoPictures.query.filter_by(id=memopic_id).first()
    if not memopic:
         return {'message' : ' memory picture not found!'}


    if not memopic.memory.user_id==current_user.id:
         return {'message' : ' memory picture not found for the current user!'}

    return memoryPicschema.dump(memopic)


@memories_pics_bp.delete('/memopicdel/<memopic_id>') #delete specific memo
@token_required
def delete(memopic_id):
    current_user = request.current_user


    memopic = MemoPictures.query.filter_by(id=memopic_id).first()
    if not memopic:
        return {'message' : ' memory pic not found '}
    if not memopic.memory.user_id==current_user.id:
        return {'message' : ' memory  pic not found for the current user '}


    result = memory_pictures_Repository.delete(memopic.id)
    if(result):
        return {"the following memory id is deleted" :f"{memopic.id}"}
    abort(404)
