from flask import Flask, request, Blueprint
from flask_restful import Resource, reqparse, abort
from flask_bcrypt import generate_password_hash
from models.UserAgenda.userAgendaModel import UserAgenda
from repositories import agendaRepository
import jwt
import datetime
from flask import Response
import json

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("id", type=int, help="id")
user_put_args.add_argument("date_time", type=datetime, help="date_time")
user_put_args.add_argument("title", type=str, help="title")
user_put_args.add_argument("user_id", type=int, help="user_id")

user_agenda_bp = Blueprint('useragenda', __name__)

@user_agenda_bp.get('')
def get():
    return agendaRepository.get_all()




@user_agenda_bp.post('')
def post():
    payload =request.get_json()
    return agendaRepository.create(payload)

@user_agenda_bp.patch('')
def patch():
    payload =request.get_json()
    return agendaRepository.update(payload)

@user_agenda_bp.delete('/<int:id>')
def delete(id):
    result = agendaRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)