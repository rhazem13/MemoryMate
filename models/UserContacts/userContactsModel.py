from models.db import db
from models.UserContacts.relationLevelEnum import ERelationLevel
class UserContacts(db.Model):
    __tablename__ = "user_contacts"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    contact_id=db.Column(db.Integer, db.ForeignKey("user.id"))
    relation=db.Column(db.Enum(ERelationLevel), nullable=False)
    bio= db.Column(db.Text())
