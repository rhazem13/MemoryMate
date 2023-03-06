from models.Memories.memoryPicsModel import MemoPictures
from models.User.userModel import User
from repositories.repository import Repository
from models.Memories.userMemoriesModel import MemoryModel

from sqlalchemy import func
from models.db import db
import json

class MemoryPicsRepository(Repository):
   def __init__(self):
        super().__init__(MemoPictures)

   def create(self,value):
        new_value = MemoPictures(**value)
        db.session.add(new_value)
        db.session.commit()
        db.session.refresh(new_value)
        return new_value

   def get_all(self):
        result = MemoPictures.query.all()
        return result

   def update(self,new_value,id):
        old_value = MemoPictures.query.get(id)
        if old_value is None:
            return False
        for key, value in new_value.items():
            setattr(old_value, key, value)
        db.session.commit()
        return old_value

   def delete(self,id):
        old_value = MemoPictures.query.get(id)
        if old_value is None:
            return False
        db.session.delete(old_value)
        db.session.commit()
        return True


   def get_by_id(id):
        result = MemoPictures.query.get(id)
        return result
   def get_by_memory_id(memory_id):
        result = MemoryModel.query.get(memory_id)
        return result
   
   
