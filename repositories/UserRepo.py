from flask_restful import fields, marshal_with
from models.db import db
from models.userModel import UserModel  
from sqlalchemy.orm import load_only


def get_all():
    result = UserModel.query.all()
    return result


def create(user):
    db.session.add(UserRepo(**user))
    db.session.commit()
    return True

def get_by_id(id):
    result = UserModel.query.get(id)
    return result

def update(new_user, id):
    user = UserModel.query.get(id)
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
    