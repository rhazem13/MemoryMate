from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.User.userTypeEnum import EUserType
from models.db import db
from models.UserLocations import userLocationsModel
from models.Notifications import notificationsModel

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False) 
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128))
    photo_path = db.Column(db.Text())
    user_type = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime(timezone=True),
                        server_default=func.now())
    locations = relationship('UserLocationModel')
    notifications = relationship('NotificationsModel')






