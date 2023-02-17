from flask_restful import fields
from models.db import db
from models.user.userModel import User  
#comment by hazem =>
#we import some models as if we don't import them they won't be noticed in the migrations
#To do : change this to db file and export them
from models.Faces.facesModel import FacesModel
from models.UserAgenda.userAgendaModel import UserAgenda
from models.UserCalendar.userCalendarModel import UserCalendarModel
from models.UserContacts.userContactsModel import UserContacts
from models.UserFaces.userfacesModel import UserfacesModel
from models.user.userTypeEnum import EUserType
from repositories.repository import Repository
from sqlalchemy.orm import load_only

class UserRepository(Repository):
   def __init__(self):
         super().__init__(User)

   def get_by_email(self,email):
      result = User.query.filter_by(email = email).first()
      return result

   def get_attr(id, attr):
      users = session.query(SomeModel).options(load_only(*fields)).all()

