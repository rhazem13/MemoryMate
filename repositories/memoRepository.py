from sqlalchemy import or_
from models.Memories.userMemoriesModel import MemoryModel
from repositories.repository import Repository, current_user_id


class MemoryRepository(Repository):
    def __init__(self):
        super().__init__(MemoryModel)

    def readable_query(self):
        user_id = current_user_id()
        return MemoryModel.query.filter(or_(
            MemoryModel.user_id == user_id,
            MemoryModel.caregivers.any(id=user_id),
        ))

    def get_readable(self, memory_id):
        return self.readable_query().filter(MemoryModel.id == memory_id).first()
