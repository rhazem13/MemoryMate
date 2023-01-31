from flask import Flask, request, Blueprint
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash
from models.user.userModel import User
from repositories import UserRepo
import jwt
import datetime
from flask import Response
import json
import random
from services.caching.caching import CacheService
from flask_caching import Cache

class UserRouters:
    user_bp = Blueprint('users', __name__)
    cache = CacheService.get_instance()
    @user_bp.get('/hello')
    @cache.get_cache(key_prefix='test_deco')
    def get():
        #get user data by id
        n = random.randint(0,10000)
        print('holaaaaaaaaaaaaaaaaaaaaaaaaaa')
        return str(n)

    @user_bp.get('/hello_update')
    @cache.update_cache(key_prefix='test_deco')
    def test_cache_update():
        n = random.randint(0,10000)
        print('holaaaaaaaaaaaaaaaaaaaaaaaaaa')
        return str(n) 

    @user_bp.post('/register')
    def register():
        payload =request.get_json()['user']
        hashed_password = generate_password_hash(payload['password'], 10)
        payload['password'] = hashed_password
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
        if password == payload['password']:
            return Response(json.dumps({'message':'success'}), status = 200, mimetype='application/json')
        return Response(status=403)

    #@user_bp.get("/me") / it returns the information of the current user based on the token

    #@user_bp.get('/locations') it returns the locations of the current user

    #@user_bp.post('/locations') it adds a location for a user
    #@user_bp.put('/locations/{location_id}') it updates a location by it's id
