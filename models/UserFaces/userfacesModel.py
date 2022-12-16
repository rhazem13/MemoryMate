from models.db import db,Base

class UserfacesModel(db.Model,Base):
    __tablename__="userfaces"
    user_id = db.Column(db.Integer,)
    face_id = db.Column(db.Integer)
    name = db.Column(db.String(20), unique=True, nullable=False)
    bio = db.Column(db.String(100), nullable=False)

