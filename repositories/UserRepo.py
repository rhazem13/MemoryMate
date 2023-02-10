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
from models.User.userTypeEnum import EUserType

from sqlalchemy.orm import load_only

resource_fields = {
    'id':fields.Integer,
    'username':fields.String,
    'firstname':fields.String,
    'lastname':fields.String,
    'email':fields.String,
    'password':fields.String,
    'photo_path':fields.String,
    'user_type':db.Enum(EUserType),
    'address':fields.String,
    'phone':fields.String,
    'date_of_birth':fields.DateTime,
    'created_at':fields.DateTime,
}


class UserRepo():

   @marshal_with(resource_fields)
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
      user = User.query.get(id)
      if user is None:
         return False
      db.session.delete(user)
      db.session.commit()
      return True

   def get_attr(id, attr):
      users = session.query(SomeModel).options(load_only(*fields)).all()

