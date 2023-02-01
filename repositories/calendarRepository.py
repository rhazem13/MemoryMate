from models.db import db
from models.UserCalendar.userCalendarModel import UserCalendarModel

def create(user):
    new_user_calendar=UserCalendarModel(**user)
    db.session.add(new_user_calendar)
    db.session.commit()
    db.session.refresh(new_user_calendar)
    return new_user_calendar

def get_all():
    result = UserCalendarModel.query.all()
    return result

def update(new_user_calendar,id):
    user_calendar = UserCalendarModel.query.get(id)
    if user_calendar is None:
        return False
    for key, value in new_user_calendar.items():
        setattr(user_calendar, key, value)
    db.session.commit()
    return user_calendar

def delete(id):
    user_calendar = UserCalendarModel.query.get(id)
    if user_calendar is None:
        return False
    db.session.delete(user_calendar)
    db.session.commit()
    return True

def get_by_id(id):
    result = UserCalendarModel.query.get(id)
    return result