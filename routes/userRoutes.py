from flask import request, Blueprint
from flask_bcrypt import generate_password_hash,check_password_hash
from middlewares.validation.userValidation import CreateUserscheme,LoginUserscheme
from repositories.userRepository import UserRepository
import jwt
import datetime
from flask import Response
from marshmallow import  ValidationError
import os
from werkzeug.utils import secure_filename
from services.caching.caching import CacheService
from services.EventEmitter.event_emitter import EventEmitter
from middlewares.auth import token_required


user_bp = Blueprint('users', __name__)
cache = CacheService.get_instance()
emitter = EventEmitter.getInstance()
create_user_schema = CreateUserscheme()
locationschema = CreateUserscheme(many=True)
login_user_schema = LoginUserscheme()
userRepository = UserRepository()
UPLOAD_FOLDER = 'static\image'

""" user_put_args = reqparse.RequestParser()

user_put_args.add_argument("username", type=str, help="email")
user_put_args.add_argument("password", type=str, help="password")
user_put_args.add_argument("password", type=str, help="firstname")
user_put_args.add_argument("password", type=str, help="lastname")
user_put_args.add_argument("password", type=str, help="date_of_birth")
user_put_args.add_argument("password", type=str, help="address")
user_put_args.add_argument("password", type=str, help="type")
 """



@user_bp.get('/currentusertest')
@token_required
def get(current_user):
  if  current_user.user_type=="PATIENT":
    return {'message': 'the user is a patient'}
  elif current_user.user_type=="CAREGIVER":
    return {'message': 'the user is a caregiver'}
  else:
    return Response(status=403)  






ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@user_bp.post('/register')
def register():
    errors = create_user_schema.validate(request.get_json())
    if errors:
        return errors,422
    payload =create_user_schema.load(request.json)
    hashed_password = generate_password_hash(payload['password']).decode('utf-8')
    payload['password'] = hashed_password
    try:
        user = userRepository.create(payload)
        return {'message': 'registered successfully'}
    except ValidationError as err:
        # print the error
        print(err.messages) 

@user_bp.post('/login')
def login():
    errors = login_user_schema.validate(request.get_json())
    if errors:
        return errors,422
    payload = login_user_schema.load(request.json)
    user = userRepository.get_by_email(payload['email'])
    if  user is None:
        return Response({"Wrong Password/Email"},status=403)  
    if check_password_hash(user.password,payload['password']):
        try:
            token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},'secret') 
            return {'token': token}
        except ValidationError as err:
            print(err.messages)
    return Response({"Wrong Password/Email"},status=403)  

@user_bp.post('/imageupload')
def test():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return {'message': 'registered successfully'}

@user_bp.get('/closefriendslocations/<int:id>')
def get_close_friends_locations(id):
    users = userRepository.get_close_friends_locations(id)
    # print(users) 
    return locationschema.dump(users)
