from flask import abort
from models.db import db
from models.Memories.memoryPicsModel import MemoPictures
from models.Memories.userMemoriesModel import MemoryModel
from repositories.memoRepository import MemoryRepository
from repositories.repository import Repository, current_user_id


class MemoryPicsRepository(Repository):
    def __init__(self):
        super().__init__(MemoPictures)

    def owned_query(self):
        return MemoPictures.query.join(MemoryModel).filter(
            MemoryModel.user_id == current_user_id())

    def readable_query(self):
        return MemoPictures.query.filter(MemoPictures.memory_id.in_(
            MemoryRepository().readable_query().with_entities(MemoryModel.id)))

    def create(self, value):
        if 'id' in value or MemoryRepository().get_by_id(value.get('memory_id')) is None:
            abort(404)
        picture = MemoPictures(**value)
        db.session.add(picture)
        db.session.commit()
        return picture
