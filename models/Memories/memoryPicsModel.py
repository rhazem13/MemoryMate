from models.db import db,Base

# from models.Memories.memoryPicsModel import Memory
class MemoPictures(db.Model,Base):
    __tablename__ = 'memory_picture'

    id = db.Column(db.Integer, primary_key=True)
    memory_id = db.Column(db.Integer, db.ForeignKey("memory.id"))
    # memory = relationship('Memory')
