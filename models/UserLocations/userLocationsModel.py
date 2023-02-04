from models.db import db,Base

class UserLocationModel(db.Model,Base):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Float)
    long = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_name=db.Column(db.String)
    additional_info = db.Column(db.Text)