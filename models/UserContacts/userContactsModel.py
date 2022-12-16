from models.db import db
from models.UserContacts.relationLevelEnum import ERelationLevel
class userContacts(db.Model):
    __tablename__ = "user_contacts"
    user_id = db.Column(db.Integer, primary_key=True)
    contact_id=db.Column(db.Integer, primary_key=True)
    relation=db.Column(db.Enum(ERelationLevel), nullable=False),
    bio=db.Column(db.text)
