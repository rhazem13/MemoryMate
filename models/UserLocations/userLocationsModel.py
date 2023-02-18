from models.db import db,Base
from geoalchemy2 import Geometry

class UserLocationModel(db.Model,Base):
    __tablename__ = "userLocations"
    id = db.Column(db.Integer, primary_key = True)
    geom = db.Column(Geometry('POINT'))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    location_name=db.Column(db.String)
    additional_info = db.Column(db.Text)