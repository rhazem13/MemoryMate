from flask import Flask, request, Blueprint,jsonify,make_response
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash,check_password_hash
from models.user.userModel import User
from validation.UserValidation import CreateUserscheme,LoginUserscheme
from repositories.UserRepo import UserRepo
import jwt
import datetime
from flask import Response
from marshmallow import  ValidationError
import os
from werkzeug.utils import secure_filename

import json
import random
from services.caching.caching import CacheService
from services.EventEmitter.event_emitter import EventEmitter
user_bp = Blueprint('users', __name__)

class UserRouters:
    user_bp = Blueprint('users', __name__)
    cache = CacheService.get_instance()
    emitter = EventEmitter.getInstance()
    @user_bp.get('/hellocache')
    #@cache.get_cache(key_prefix='test_deco')
    def getcache():
        #get user data by id
        n = random.randint(0,10000)
        print('holaaaaaaaaaaaaaaaaaaaaaaaaaa')
        UserRouters.emitter.emit('an-event', keyword=3, name="sharaf")
        return str(n)

"""user_put_args.add_argument("username", type=str, help="email")
user_put_args.add_argument("password", type=str, help="password")
user_put_args.add_argument("password", type=str, help="firstname")
user_put_args.add_argument("password", type=str, help="lastname")
user_put_args.add_argument("password", type=str, help="date_of_birth")
user_put_args.add_argument("password", type=str, help="address")
user_put_args.add_argument("password", type=str, help="type")
 """


   




@user_bp.get('/hello')
def get():
    #get user data by id
    return "alaaaaa"



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@user_bp.post('/register')
def register():

    payload =request.get_json()['user']
    create_user_schema = CreateUserscheme()
    hashed_password = generate_password_hash(payload['password']).decode('utf-8')
    payload['password'] = hashed_password

    errors = create_user_schema.validate(payload)

    if errors:
        return errors,422
    try:
     user = UserRepo.create(payload)
     return {'message': 'registered successfully'}
    
    except ValidationError as err:
    # print the error
     print(err.messages) 

UPLOAD_FOLDER = 'static\image'
@user_bp.post('/imageupload')
def test():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return {'message': 'registered successfully'}

    

    





login_user_schema = LoginUserscheme()
@user_bp.post('/login')
def login():
    payload = request.get_json()['user']
    user = UserRepo.get_by_email(payload['email'])
    errors = login_user_schema.validate(payload)

    if errors:
        return errors,422
    elif  user is None:
        return Response(status = 404)   

    if check_password_hash( user.password,payload['password']):
        try:
         token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},'secret') 
         return {'token': token}
        except ValidationError as err:
            print(err.messages)

    return Response(status=403)  
    @user_bp.get('/hello')
    def get():
        #get user data by id
        return "alaaaaa"

    @user_bp.post('/register')
    def register():
        payload =request.get_json()['user']
        hashed_password = generate_password_hash(payload['password']).decode('utf-8')
        payload['hashed_password'] = hashed_password
        user = UserRepo.create(payload)
        return {'message': 'registered successfully'}

    @user_bp.post('/login')
    def login():
        payload = request.get_json()['user']
        user = UserRepo.get_by_email(payload['email'])
        if  user is None:
            return Response(status = 404)   
        print(payload['password'].encode('utf-8'))
        print('#################')
        print(user.hashed_password)
        if check_password_hash( user.hashed_password,payload['password']):
            token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},'secret') 
            return {'token': token}
        return Response(status=403)  
    
    
   

    #@user_bp.get("/me") / it returns the information of the current user based on the token

    #@user_bp.get('/locations') it returns the locations of the current user

    #@user_bp.post('/locations') it adds a location for a user
    #@user_bp.put('/locations/{location_id}') it updates a location by it's id
