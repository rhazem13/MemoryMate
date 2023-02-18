
from models.db import db,Base


class CaregiverMemory(db.Model,Base):
    __tablename__ = "caregiverMemory"
    id = db.Column(db.Integer, primary_key = True)
    memory_id = db.Column(db.Integer, db.ForeignKey("memory.id"))
    caregiver_id = db.Column(db.Integer, db.ForeignKey("user.id"))