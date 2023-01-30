from flask_restful import fields, marshal_with
from models.db import db
from models.User.userModel import User  
#comment by hazem =>
#we import some models as if we don't import them they won't be noticed in the migrations
#To do : change this to db file and export them
from models.Faces.facesModel import FacesModel
from models.UserAgenda.userAgendaModel import UserAgenda
from models.UserCalendar.userCalendarModel import UserCalendarModel
from models.UserContacts.userContactsModel import UserContacts
from models.UserFaces.userfacesModel import UserfacesModel

from sqlalchemy.orm import load_only


def get_all():
    result = User.query.all()
    return result


def create(user):
    new_user = User(**user)
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)
    return new_user

def get_by_id(id):
    result = User.query.get(id)
    return result

def get_by_email(email):
    result = User.query.filter_by(email = email).first()
    return result

def update(new_user, id):
    user = User.query.get(id)
    if user is None:
        return False
    for key, value in new_user.items():
        setattr(user, key, value)
    db.session.commit()
    return True

def delete(id):
    user = UserModel.query.get(id)
    if user is None:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

def get_attr(id, attr):
    users = session.query(SomeModel).options(load_only(*fields)).all()
    