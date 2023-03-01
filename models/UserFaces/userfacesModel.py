from models.db import db,Base

class UserfacesModel(db.Model,Base):
    __tablename__="userfaces"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    face_url = db.Column(db.String(100))
    name = db.Column(db.String(20), nullable=False)
    bio = db.Column(db.String(100), nullable=False)

