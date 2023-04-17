
from models.db import db,Base
#from models.Memories.userMemoriesModel import MemoryModel


class CaregiverMemory(db.Model,Base):
    __tablename__ = "caregiverMemory"
    memory_id = db.Column(db.Integer, db.ForeignKey("memory.id"),primary_key=True)
    caregiver_id = db.Column(db.Integer, db.ForeignKey("user.id"),primary_key=True)
    #user = db.relationship(User, backref=db.backref("care giver memories", cascade="all, delete-orphan"))
    # memory = db.relationship(MemoryModel, backref=db.backref("care giver memories", cascade="all, delete-orphan"))
