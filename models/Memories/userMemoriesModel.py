from models.db import db,Base
from models.Memories.memoryPicsModel import MemoPictures
from models.Memories.caregiversMemoriesModel import CaregiverMemory
from models.User.userModel import User

class MemoryModel(db.Model,Base):
    __tablename__ = "memory"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title=db.Column(db.String)
    memo_body=db.Column(db.String)
    memo_date = db.Column(db.Date, nullable=True)
    thumbnail=db.Column(db.String)
    pictures = db.relationship('MemoPictures',back_populates='memory') 
    caregivers=db.relationship("User",secondary="caregiverMemory",back_populates='caregiver_memories')

    





    #caregiver=db.relationship('User',secondary="care_giver_memories",back_populates="memories")

#backpopulate:creates a fake column in both tables to get any memory or picture details from the other table
