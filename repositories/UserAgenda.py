from flask_restful import fields, marshal_with
from models.db import db
from models.userAgenda.userAgendaModel import UserAgenda

resource_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'ocassion': fields.String,
}
@marshal_with(resource_fields)
def get_all():
    result = UserAgenda.query.all()
    return result


def create(user):
    db.session.add(UserAgenda(**user))
    db.session.commit()
    return True

@marshal_with(resource_fields)
def get_by_id(id):
    result = UserAgenda.query.get(id)
    return result
