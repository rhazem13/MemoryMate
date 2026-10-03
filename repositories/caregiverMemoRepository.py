from flask import abort
from models.Memories.caregiversMemoriesModel import CaregiverMemory
from models.db import db
from repositories.memoRepository import MemoryRepository


class caregiverMemoryRepository:
    def delete(self, memory_id, caregiver_id):
        if MemoryRepository().get_by_id(memory_id) is None:
            abort(404)
        share = db.session.get(CaregiverMemory, (int(memory_id), int(caregiver_id)))
        if share is None:
            return False
        db.session.delete(share)
        db.session.commit()
        return True
