from flask import Flask, request
from flask_restful import Resource, reqparse, abort
from models.userModel import User


class UserRouter(Resource):
    
    def get(self, id):
        #get user data by id
        return 1

    def patch(self, id):
        #modify user data by id
        return 1
    
    def delete(self,id):
        #delete user by id
        return 1