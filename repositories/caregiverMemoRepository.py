from models.Memories.caregiversMemoriesModel import CaregiverMemory
from models.User.userModel import User
from repositories.repository import Repository
from sqlalchemy import func
from models.db import db
import json

class MemoryRepository(Repository):
   def __init__(self):
        super().__init__(CaregiverMemory)

   def create(self,value):
        new_value = CaregiverMemory(**value)
        db.session.add(new_value)
        db.session.commit()
        db.session.refresh(new_value)
        return new_value

   def get_all(self):
        result = CaregiverMemory.query.all()
        return result

   def update(self,new_value,id):
        old_value = CaregiverMemory.query.get(id)
        if old_value is None:
            return False
        for key, value in new_value.items():
            setattr(old_value, key, value)
        db.session.commit()
        return old_value

   def delete(self,id):
        old_value = CaregiverMemory.query.get(id)
        if old_value is None:
            return False
        db.session.delete(old_value)
        db.session.commit()
        return True


   def get_by_id(id):
        result = CaregiverMemory.query.get(id)
        return result
   
