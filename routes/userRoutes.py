from flask import Flask, request
from flask_restful import Resource, reqparse, abort
from models.user.userModel import User


class UserRouter(Resource):
    
    def get(self):
        #get user data by id
        return "shaaf"

    def patch(self):
        #modify user data by id
        return 1
    
    def delete(self):
        #delete user by id
        return 1