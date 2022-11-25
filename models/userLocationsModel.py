from models.db import db
class Location(db.Model):
    __tablename__ = "locations"
    id = db.Column(db.Integer, primary_key = True)
    lat = db.Column(db.Float)
    lang = db.Column(db.Float)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))