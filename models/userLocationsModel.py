from models.db import db,Base

class UserLocationModel(db.Model,Base):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Float)
    lang = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))