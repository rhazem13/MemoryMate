from flask import Flask, request, Blueprint
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash
from models.user.userModel import User
from repositories import UserRepo
import jwt
import datetime
from flask import Response
import json
user_bp = Blueprint('users', __name__)

""" user_put_args = reqparse.RequestParser()

user_put_args.add_argument("username", type=str, help="email")
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
    return "shaaf"

@user_bp.post('/register')
def register():
    payload =request.get_json()['user']
    hashed_password = generate_password_hash(payload['hashed_password'], 10)
    payload['hashed_password'] = "123456"
    user = UserRepo.create(payload)
    token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},'secret')
    return {'token': token}

@user_bp.post('/login')
def login():
    payload = request.get_json()['user']
    user = UserRepo.get_by_email(payload['email'])
    if  user is None:
        return Response(status = 404)
    password = user.hashed_password
    if password == payload['hashed_password']:
        return Response(json.dumps({'message':'success'}), status = 200, mimetype='application/json')
    return Response(status=403)


def delete(self):
    #delete user by id
    return 1