from models.Memories.caregiversMemoriesModel import CaregiverMemory
from repositories.repository import Repository
from sqlalchemy import func
from models.db import db
import json

class caregiverMemoryRepository(Repository):
   def __init__(self):
        super().__init__(CaregiverMemory)

   def delete(self,memory_id,caregiver_id):
        old_value = CaregiverMemory.query.get((memory_id,caregiver_id))
        if old_value is None:
            return False
        db.session.delete(old_value)
        db.session.commit()
        return True


   def get_by_id(self,memory_id,caregiver_id):
        result = CaregiverMemory.query.get((memory_id,caregiver_id))
        return result
   
