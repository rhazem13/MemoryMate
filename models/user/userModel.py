from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.user.userTypeEnum import EUserType
from models.db import db
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)
    address = db.Column(db.String(100), nullable=False)
    type = db.Column(db.Enum(EUserType), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                        server_default=func.now())
    bio = db.Column(db.Text)
    locations = relationship('Locations')
    notifications = relationship('notifications')
    email = db.Column(db.String(255))
    hashed_password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                        server_default=func.now())
