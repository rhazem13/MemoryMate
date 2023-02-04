from models.db import db,Base

class UserfacesModel(db.Model,Base):
    __tablename__="userfaces"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    face_id = db.Column(db.Integer,db.ForeignKey("faces.id"))
    name = db.Column(db.String(20), unique=True, nullable=False)
    bio = db.Column(db.String(100), nullable=False)

