from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.user.userTypeEnum import EUserType
from models.db import db
from geoalchemy2 import Geometry
from models.Memories.caregiversMemoriesModel import CaregiverMemory
from models.user.userTypeEnum import EUserType
from sqlalchemy import Enum

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
    photo_path = db.Column(db.Text())
    user_type = db.Column(db.String(20))
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),server_default=func.now())
    locations = relationship('UserLocationModel')
    #notifications = relationship('NotificationsModel')
    caregiver_memories=db.relationship("MemoryModel",secondary="caregiverMemory",back_populates='caregivers')
    patient_memories=db.relationship('MemoryModel',backref='patient')



    # location = db.Column(Geometry('POINT'))

    # backref:establishes a collection of memories objects on User called User.memories. 
    # It also establishes a .patient attribute on memory which will refer to the parent User object. 
