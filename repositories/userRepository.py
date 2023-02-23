from flask_restful import fields
from models.db import db
from models.User.userModel import User  
from models.UserContacts.userContactsModel import UserContacts  
#comment by hazem =>
#we import some models as if we don't import them they won't be noticed in the migrations
#To do : change this to db file and export them
from models.Memories.caregiversMemoriesModel import CaregiverMemory
from models.Memories.memoryPicsModel import MemoPictures
from models.Memories.userMemoriesModel import MemoryModel
from models.UserFaces.userfacesModel import UserfacesModel
from models.UserAgenda.userAgendaModel import UserAgenda
from models.UserCalendar.userCalendarModel import UserCalendarModel
from models.UserContacts.userContactsModel import UserContacts
from models.UserFaces.userfacesModel import UserfacesModel
from models.User.userTypeEnum import EUserType
from repositories.repository import Repository
from repositories.contactsRepository import ContactsRepository
from sqlalchemy.orm import load_only
from sqlalchemy import func
from repositories.contactsRepository import ContactsRepository

contactsRepository = ContactsRepository

class UserRepository(Repository):
   def __init__(self):
         super().__init__(User)

   def get_all(self):
      result = User.query.with_entities(User.username,User.firstname,User.lastname,User.user_type,User.address,User.phone,
      User.password,User.date_of_birth,User.email,
      func.ST_AsGeoJSON(func.ST_Envelope(User.location)).label('location')).all()
      return result

   def get_close_friends_locations(self,id):
      user = User.query.get(id)
      contactslist = UserContacts.query.filter(UserContacts.user_id==id).with_entities(UserContacts.contact_id).all()
      newlist = [sublist[0] for sublist in contactslist]
      print(2 in newlist)
      result = User.query.with_entities(User.username,User.firstname,User.lastname,User.user_type,User.address,User.phone,
      User.password,User.date_of_birth,User.email,
      func.ST_AsGeoJSON(func.ST_Envelope(User.location)).label('location')).filter(User.id.in_(newlist)).order_by(User.location.distance_box(user.location)).limit(10).all()
      print(result)
      return result

   def get_by_email(self,email):
      result = User.query.filter_by(email = email).first()
      return result
   def get_by_id(self,id):
        result = User.query.get(id)
        return result

   def get_attr(id, attr):
      users = session.query(SomeModel).options(load_only(*fields)).all()
   
   def get_patients_by_caregiver_id(self, id):
      result = contactsRepository.get_patients_ids(id)
      idlist = [sublist[0] for sublist in result]
      patients = User.query.with_entities(User.username,User.firstname,User.lastname,User.user_type,User.address,User.phone,
      User.password,User.date_of_birth,User.email,
      func.ST_AsGeoJSON(func.ST_Envelope(User.location)).label('location')).filter(User.id.in_(idlist)).all()
      return patients

   def get_caregivers_by_patient_id(patient_id):
      contacts = ContactsRepository.findByUserId(patient_id)
      print('contacts are ',contacts)
      ids = list()
      for contact in contacts:
         ids.append(contact.contact_id)
      result = User.query.filter(User.id.in_(ids)).all()
      return result 

