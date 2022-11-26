from flask import Flask, request
from flask_restful import Resource, reqparse, abort
from models.userModel import UserModel

class UserRouter(Resource):
    
    def get(self):
        #get user data by id
        return 1

    def patch(self):
        #modify user data by id
        return 1
    
    def delete(self):
        #delete user by id
        return 1