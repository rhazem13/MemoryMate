from models.db import db
from models.UserAgenda.userAgendaModel import UserAgenda

def create(user):
    new_user_agenda=UserAgenda(**user)
    db.session.add(new_user_agenda)
    db.session.commit()
    db.session.refresh(new_user_agenda)
    return new_user_agenda

def get_all():
    result = UserAgenda.query.all()
    return result

def update(new_user_agenda,id):
    user_agenda = UserAgenda.query.get(id)
    if user_agenda is None:
        return False
    for key, value in new_user_agenda.items():
        setattr(user_agenda, key, value)
    db.session.commit()
    return user_agenda

def delete(id):
    user_agenda = UserAgenda.query.get(id)
    if user_agenda is None:
        return False
    db.session.delete(user_agenda)
    db.session.commit()
    return True

def get_by_id(id):
    result = UserAgenda.query.get(id)
    return result