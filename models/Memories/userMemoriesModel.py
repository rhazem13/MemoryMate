from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.db import db,Base
from models.Memories.memoryPicsModel import MemoPictures
import sqlalchemy_imageattach
from sqlalchemy_imageattach.entity import image_attachment
from flask_wtf.file import FileField ,FileAllowed

class Memory(db.Model,Base):
    __tablename__ = "memory"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title=db.Column(db.String)
    memo_body=db.Column(db.String)
    memo_date = db.Column(db.Date, nullable=True)
    thumbnail=db.Column()
    memo_pic = image_attachment('MemoPictures')

sqlalchemy_imageattach.stores.fs.FileSystemStore(
    path='\MemoryMate\MemoryMate\images',
    base_url='http://172.0.0.1/'
)



 











