from flask import Flask, request, Blueprint,jsonify,make_response
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash,check_password_hash
from models.user.userModel import User
from validation.UserValidation import CreateUserscheme,LoginUserscheme
from middlewares.auth import *
from repositories.UserRepo import UserRepo
import jwt
import datetime
from flask import Response
from marshmallow import  ValidationError
import os
from werkzeug.utils import secure_filename


user_bp = Blueprint('users', __name__)
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



@user_bp.get('/auth')
@token_required
def get():
    return {'message': 'authinticated successfully'}



ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@user_bp.post('/register')
def register():

    payload =request.get_json()['user']
    create_user_schema = CreateUserscheme()
    hashed_password = generate_password_hash(payload['password']).decode('utf-8')
    errors = create_user_schema.validate(payload)
    if errors:
        return errors,422

    try:
     payload['password'] = hashed_password
     user = UserRepo.create(payload)
     return {'message': 'registered successfully'}
    
    except ValidationError as err:
    # print the error
     print(err.messages) 

@user_bp.post('/imageupload')
def test():
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    return {'message': 'registered successfully'}

# @user_bp.get('/protected')
# @token_required
# def get():
#         return "protected"

# @user_bp.get('/unprotected')
# def get():
#         return "unprotected"




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
         return jsonify({'token' : token})
        except ValidationError as err:
            print(err.messages)

    return Response(status=403)  
    
    
   

#@user_bp.get("/me") / it returns the information of the current user based on the token

#@user_bp.get('/locations') it returns the locations of the current user

#@user_bp.post('/locations') it adds a location for a user
#@user_bp.put('/locations/{location_id}') it updates a location by it's id
