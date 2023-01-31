from flask_restful import fields, marshal_with
from models.db import db
from models.UserCalendar.userCalendarModel import UserCalendarModel

resource_fields = {
    'id': fields.Integer,
    'date': fields.DateTime,
    'title': fields.String,
    'user_id':fields.Integer,
    'additional_info':fields.String
}

@marshal_with(resource_fields)
def get_all():
    result = UserCalendarModel.query.all()
    return result

@marshal_with(resource_fields)
def create(user):
    new_user_calendar=UserCalendarModel(**user)
    db.session.add(new_user_calendar)
    db.session.commit()
    db.session.refresh(new_user_calendar)
    return new_user_calendar

@marshal_with(resource_fields)
def get_by_id(id):
    result = UserCalendarModel.query.get(id)
    return result

def delete(id):
    user_calendar = UserCalendarModel.query.get(id)
    if user_calendar is None:
        return False
    db.session.delete(user_calendar)
    db.session.commit()
    return True


@marshal_with(resource_fields)
def update(new_user_calendar):
    user_calendar = UserCalendarModel.query.get(new_user_calendar['id'])
    if user_calendar is None:
        return False
    for key, value in new_user_calendar.items():
        setattr(user_calendar, key, value)
    db.session.commit()
    return True
