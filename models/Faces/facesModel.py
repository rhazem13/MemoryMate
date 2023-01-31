from models.db import db,Base

class FacesModel(db.Model,Base):
    __tablename__= "faces"
    id = db.Column(db.Integer, primary_key = True)
    type = db.Column(db.Text)