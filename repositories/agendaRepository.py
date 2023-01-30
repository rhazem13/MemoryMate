from flask_restful import fields, marshal_with
from models.db import db
from models.UserAgenda.userAgendaModel import UserAgenda

resource_fields = {
    'id': fields.Integer,
    'date_time': fields.DateTime,
    'title': fields.String,
    'user_id':fields.Integer,
}

@marshal_with(resource_fields)
def get_all():
    result = UserAgenda.query.all()
    return result

@marshal_with(resource_fields)
def create(user):
    new_user_agenda=UserAgenda(**user)
    db.session.add(new_user_agenda)
    db.session.commit()
    db.session.refresh(new_user_agenda)
    return new_user_agenda

@marshal_with(resource_fields)
def get_by_id(id):
    result = UserAgenda.query.get(id)
    return result

def delete(id):
    user_agenda = UserAgenda.query.get(id)
    if user_agenda is None:
        return False
    db.session.delete(user_agenda)
    db.session.commit()
    return True


@marshal_with(resource_fields)
def update(new_user_agenda):
    user_agenda = UserAgenda.query.get(new_user_agenda['id'])
    if user_agenda is None:
        return False
    for key, value in new_user_agenda.items():
        setattr(user_agenda, key, value)
    db.session.commit()
    return True
