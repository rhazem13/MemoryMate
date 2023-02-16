from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.db import db
from models.Memories.memoryPicsModel import Memory
from sqlalchemy_imageattach.entity import Image, image_attachment
class MemoPictures(Image):
    __tablename__ = 'memory_picture'

    id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    memory = relationship('Memory')
