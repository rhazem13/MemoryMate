from flask import Flask, request, Blueprint,jsonify,make_response,session
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash,check_password_hash
from models.user.userModel import User
from validation.UserValidation import *
from middlewares.auth import *
from repositories.UserRepo import UserRepo
import jwt
import datetime,time,random
from flask import Response
from marshmallow import  ValidationError
import os
from werkzeug.utils import secure_filename
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from models.db import db
from dotenv import load_dotenv


load_dotenv()
user_bp = Blueprint('users', __name__)
UPLOAD_FOLDER = 'static\image'
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN= os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID= os.environ.get('VERIFY_SERVICE_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)



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
         token = jwt.encode({'id' : user.id},'secret') #, 'exp' : datetime.datetime.utcnow() + datetime.timedelta()
         return jsonify({'token' : token})
        except ValidationError as err:
            print(err.messages)

    return Response(status=403)  




create_validation_schema = CreateResetPasswordEmailSendInputSchema()
@user_bp.post('/reset')
def reset():
    payload =request.get_json()['user']
    user = UserRepo.get_by_email(payload['email'])
    errors = create_validation_schema.validate(payload)
    channel=payload['channel']
    if errors:
        return errors,422
    elif user is None:
        return 404
    phone_number=user.phone
    print("ok")
    client.verify \
        .services(VERIFY_SERVICE_SID) \
        .verifications \
        .create(to=phone_number, channel=channel)
    return {'message': 'sent successfully'}



@user_bp.post('/verify')
def verify():
    
    payload =request.get_json()['user']
    user = UserRepo.get_by_email(payload['email'])
    phone_number=user.phone
    verification_code = payload['verificationcode']
    error = None
    if check_verification_token(phone_number,verification_code):
     return {'message': 'auhinticated successfully'}
    
    error = "Invalid verification code. Please try again."
    return {'message': error }
def check_verification_token(phone_number,verification_code):
     check = client.verify \
        .services(VERIFY_SERVICE_SID) \
        .verification_checks \
        .create(to=phone_number, code=verification_code)       
     return check.status == 'approved'


@user_bp.post('/newpass')    
def newpass():
    payload =request.get_json()['user']
    create_validation_schema = ResetPasswordInputSchema()
    errors = create_validation_schema.validate(payload)
    token = request.headers['x-access-token']
    if errors:
        return errors,422
    if not token:
        return  {"message":"Token is required!"}
    token= jwt.decode(token,'secret', algorithms=['HS256'])
    user = User.query.filter_by(id=token['id']).first()
    if user is None:
        return{"message":"No record found with this email. please signup first"}
    user = User.query.filter_by(id=token['id']).first()
    user.password=generate_password_hash(payload['password']).decode('utf-8')
    db.session.commit()

    return{"message":"New password SuccessFully set."}



         


    
    
    
    
       
    
    
   

#@user_bp.get("/me") / it returns the information of the current user based on the token

#@user_bp.get('/locations') it returns the locations of the current user

#@user_bp.post('/locations') it adds a location for a user
#@user_bp.put('/locations/{location_id}') it updates a location by it's id
# def resetcode():
#      email=None
#      payload['email']=email
#  def get_unique_id(email):
#        number= str(int(abs(hash(email))+time.time()))
#        if len(number)<8:
#          number=number+str(random(8-len(number)))
#        return number[:8]
