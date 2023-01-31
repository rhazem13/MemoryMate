from flask import Flask, request, Blueprint
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash
from models.UserCalendar.userCalendarModel import UserCalendarModel
from repositories import calendarRepository
import jwt
import datetime
from flask import Response
import json

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("id", type=int, help="id")
user_put_args.add_argument("date", type=datetime, help="date_time")
user_put_args.add_argument("title", type=str, help="title")
user_put_args.add_argument("user_id", type=int, help="user_id")
user_put_args.add_argument("additional_info", type=str, help="additional_info")

user_calendar_bp = Blueprint('usercalendar', __name__)

@user_calendar_bp.get('')
def get():
    return calendarRepository.get_all()




@user_calendar_bp.post('')
def post():
    payload =request.get_json()
    return calendarRepository.create(payload)

@user_calendar_bp.patch('')
def patch():
    payload =request.get_json()
    return calendarRepository.update(payload)

@user_calendar_bp.delete('/<int:id>')
def delete(id):
    result = calendarRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)