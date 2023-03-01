from flask import Flask, request, Blueprint, jsonify, make_response, session
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash, check_password_hash
from models.User.userModel import User
from repositories.userRepository import UserRepository
from middlewares.validation.userValidation import *
from repositories.userRepository import UserRepository
from middlewares.auth import *
import jwt
import datetime
import time
import random
from flask import Response
from marshmallow import ValidationError
import os
from werkzeug.utils import secure_filename
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from models.db import db
from dotenv import load_dotenv
from services.caching.caching import CacheService
from services.EventEmitter.event_emitter import EventEmitter
from middlewares.auth import token_required
import logging


load_dotenv()
user_bp = Blueprint('users', __name__)
cache = CacheService.get_instance()
emitter = EventEmitter.getInstance()
create_user_schema = CreateUserscheme()
locationschema = CreateUserscheme(many=True)
login_user_schema = LoginUserscheme()
codetoEmailSend_validation_schema = CreateResetPasswordEmailSendInputSchema()
verify_validation_schema = VerifyEmailaddress()
newpass_validation_schema = ResetPasswordInputSchema()
LOG = logging.getLogger('alerta.plugins.twilio')


userRepository = UserRepository()
UPLOAD_FOLDER = 'static\image'
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
VERIFY_SERVICE_SID = os.environ.get('VERIFY_SERVICE_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@user_bp.get('/currentusertest')
@token_required
def get():
    current_user = request.current_user
    if current_user.user_type == "PATIENT":
        return {'message': 'the user is a patient'}
    elif current_user.user_type == "CAREGIVER":
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
        return errors, 422
    payload = create_user_schema.load(request.json)

    hashed_password = generate_password_hash(
        payload['password']).decode('utf-8')
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
        return errors, 422
    payload = login_user_schema.load(request.json)
    user = userRepository.get_by_email(payload['email'])
    if user is None:
        return Response({"Wrong Password/Email"}, status=403)
    if check_password_hash(user.password, payload['password']):
        try:
            # , 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            token = jwt.encode({'id': user.id}, 'secret')
            return {'token': token}
        except ValidationError as err:
            print(err.messages)
    return Response({"Wrong Password/Email"}, status=403)


@user_bp.post('/imageupload')
def test():
    file = request.files['file']
    file_name = secure_filename(file.filename)
    file_path = UPLOAD_FOLDER + file.filename
    file.save(UPLOAD_FOLDER + file_name)
    print(file_path)
    return {'message': 'uploaded successfully'}


@user_bp.post('/EmailSend')
def reset():
    try:

        payload = request.get_json()['user']
        user = UserRepository().get_by_email(payload['email'])
        errors = codetoEmailSend_validation_schema.validate(payload)
        channel = payload['channel']

        if errors:
            return errors, 422
        if user is None:
            return {'message': 'wrong email address , please send a correct email address'}

        phone_number = user.phone
        client.verify \
            .services(VERIFY_SERVICE_SID) \
            .verifications \
            .create(to=phone_number, channel=channel)
        return {'message': 'sent successfully'}
    except KeyError as Ke:
        return {'message': "please send your "+str(Ke)}


@user_bp.post('/verify')
def verify():

    try:
        payload = request.get_json()['user']

        ValidationError = verify_validation_schema.validate(payload)
        if ValidationError:
            return ValidationError, 422

        user = UserRepository().get_by_email(payload['email'])
        if user is None:
            return {'message': 'wrong email address , please send a correct email address'}
        phone_number = user.phone
        verification_code = payload['verificationcode']
        verificationcode_error = None

        try:
            check = client.verify \
                .services(VERIFY_SERVICE_SID) \
                .verification_checks \
                .create(to=phone_number, code=verification_code)

            if check.status == 'approved':
                # , 'exp' : datetime.datetime.utcnow() + datetime.timedelta()
                token = jwt.encode({'id': user.id}, 'secret')
                return jsonify({'token': token})

            else:
                verificationcode_error = "Invalid verification code. Please try again."
                return {'message': verificationcode_error}

        except TwilioRestException as e:
            return "Error validating code: {}".format(e)

    except KeyError as Ke:
        return {'message': "please send your correct "+str(Ke)}


@user_bp.post('/newpass')
def newpass():
    payload = request.get_json()['user']
    errors = newpass_validation_schema.validate(payload)
    token = request.headers['x-access-token']
    if errors:
        return errors, 422
    elif not token:
        return {"message": "Token is required!"}

    token = jwt.decode(token, 'secret', algorithms=['HS256'])
    user = User.query.filter_by(id=token['id']).first()
    if user is None:
        return{"message": "No record found with this email. please signup first"}
    user.password = generate_password_hash(payload['password']).decode('utf-8')
    db.session.commit()
    return{"message": "New password SuccessFully set."}


# @user_bp.get("/me") / it returns the information of the current user based on the token

# @user_bp.get('/locations') it returns the locations of the current user

# @user_bp.post('/locations') it adds a location for a user
# @user_bp.put('/locations/{location_id}') it updates a location by it's id
# def resetcode():
#      email=None
#      payload['email']=email
#  def get_unique_id(email):
#        number= str(int(abs(hash(email))+time.time()))
#        if len(number)<8:
#          number=number+str(random(8-len(number)))
#        return number[:8]
@user_bp.get('/closefriendslocations/<int:id>')
def get_close_friends_locations(id):

    users = userRepository.get_close_friends_locations(id)
<<<<<<< HEAD
    # print(users) 
    return locationschema.dump(users)

=======
    # print(users)
    return locationschema.dump(users)
>>>>>>> 9daca5f8d62aba96d1dd97eb6183e932060e7b93
