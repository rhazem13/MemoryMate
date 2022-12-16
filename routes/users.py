from flask import request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, reqparse, abort
from repositories import UserRepo
from models.user import userModel
from models.db import db
from middlewares.auth import token_required
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("id", type=int, help="id")

#user_put_args.add_argument("public_id", type=int, help="id")

user_put_args.add_argument("username", type=str, help="username")
user_put_args.add_argument("password", type=str, help="password")

class AdminRegisterRouter(Resource):

    @token_required
    def get(current_user):
        
        # if not current_user.admin:
        #return jsonify({'message' : 'Cannot perform that function!'})

       
        return UserRepo.get_all()

    def post(current_user):

        return request.get_json()
        """  args = user_put_args.parse_args()
        hashed_password = generate_password_hash(args['password'], method='sha256')
        new_user = UserRepo(public_id=str(uuid.uuid4()), name=args['name'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit() """
    
    def login():
       auth = request.authorization

       if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

       user = UserRepo.query.filter_by(name=auth.username).first()

       if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

       if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},'secret')

        return jsonify({'token' : token.decode('UTF-8')})

       return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})


        