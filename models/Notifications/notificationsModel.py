# ...
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models.db import db,Base
from sqlalchemy.dialects.postgresql import JSONB


class notificationsModel(db.Model,Base):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title = db.Column(db.Text)
    #body should be object like {data:"enta nset t3ml project 7sen", sender:"Momen"},
    body =  db.Column(db.JSONB)
    created_at = db.Column(db.DateTime(timezone=True),
                        server_default=func.now())
    type = db.String(100)
    
