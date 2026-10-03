from flask_restful import fields
from models.db import db
from models.user.userModel import User  
from models.UserContacts.userContactsModel import UserContacts  
#comment by hazem =>
#we import some models as if we don't import them they won't be noticed in the migrations
#To do : change this to db file and export them
from models.Memories.memoryPicsModel import MemoPictures
from models.Memories.userMemoriesModel import MemoryModel
from models.UserFaces.userfacesModel import UserfacesModel
from models.UserAgenda.userAgendaModel import UserAgenda
from models.UserCalendar.userCalendarModel import UserCalendarModel
from models.UserContacts.userContactsModel import UserContacts
from models.UserFaces.userfacesModel import UserfacesModel
from models.user.userTypeEnum import EUserType
from repositories.repository import Repository
from repositories.repository import current_user_id
from flask import abort
from repositories.contactsRepository import ContactsRepository
from sqlalchemy.orm import load_only
from sqlalchemy import func
from repositories.contactsRepository import ContactsRepository
from services.photoservice.photoservice import PhotoService
photoservice= PhotoService()
contactsRepository = ContactsRepository

class UserRepository(Repository):
   def __init__(self):
         super().__init__(User)

   def get_close_friends_locations(self, id):
      if int(id) != current_user_id():
         abort(404)
      from repositories.locationRepository import LocationRepository
      return LocationRepository().get_caregivers_location(id)

   def get_by_email(self,email):
      result = User.query.filter_by(email = email).first()
      return result
   def get_by_id(self,id):
      result = User.query.get(id)
      return result

   def create(self, data):
      allowed = {'full_name', 'email', 'password', 'photo_path', 'user_type',
                 'address', 'phone', 'date_of_birth'}
      if not set(data).issubset(allowed):
         abort(422)
      user = User(**data)
      db.session.add(user)
      db.session.commit()
      return user
   
   def patch(self,id,data):
      if int(id) != current_user_id():
         abort(404)
      allowed = {'full_name', 'address', 'phone', 'date_of_birth'}
      if not set(data).issubset(allowed):
         abort(422)
      user = db.session.get(User, id)
      for key, value in data.items():
         setattr(user, key, value)
      db.session.commit()
      return user

   def changephoto(self,id,newphoto):
      if int(id) != current_user_id():
         abort(404)
      user = User.query.get(id)
      newphotopath = photoservice.addPhoto(newphoto,"users")
      setattr(user, "photo_path", newphotopath)
      db.session.commit()
      return user

   def get_patients_by_caregiver_id(self, id):
      if int(id) != current_user_id():
         abort(404)
      return User.query.join(UserContacts, UserContacts.user_id == User.id).filter(
         UserContacts.contact_id == id).all()

   @staticmethod
   def get_caregivers_by_patient_id(patient_id):
      return User.query.join(UserContacts, UserContacts.contact_id == User.id).filter(
         UserContacts.user_id == patient_id).all()
