from models.db import db
from models.UserContacts.relationLevelEnum import ERelationLevel
from sqlalchemy import Enum

class UserContacts(db.Model):
    __tablename__ = "user_contacts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    contact_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    relation=db.Column(Enum(ERelationLevel))
    bio= db.Column(db.Text())