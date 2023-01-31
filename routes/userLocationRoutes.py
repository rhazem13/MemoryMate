from flask import Flask, request, Blueprint
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash
from models.UserLocations.userLocationsModel import UserLocationModel
from repositories import locationRepository
import jwt
import datetime
from flask import Response
import json


user_put_args = reqparse.RequestParser()
user_put_args.add_argument("id", type=int, help="id")
user_put_args.add_argument("lat", type=float, help="lat")
user_put_args.add_argument("long", type=float, help="long")
user_put_args.add_argument("user_id", type=int, help="user_id")
user_put_args.add_argument("location_name", type=str, help="location_name")
user_put_args.add_argument("additional_info", type=str, help="additional_info")


user_location_bp = Blueprint('userlocation', __name__)

@user_location_bp.get('')
def get():
    return locationRepository.get_all()




@user_location_bp.post('')
def post():
    payload =request.get_json()
    return locationRepository.create(payload)

@user_location_bp.patch('')
def patch():
    payload =request.get_json()
    return locationRepository.update(payload)

@user_location_bp.delete('/<int:id>')
def delete(id):
    return locationRepository.delete(id)