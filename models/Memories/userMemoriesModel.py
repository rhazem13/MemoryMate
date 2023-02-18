from models.db import db,Base

class Memory(db.Model,Base):
    __tablename__ = "memory"
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    title=db.Column(db.String)
    memo_body=db.Column(db.String)
    memo_date = db.Column(db.Date, nullable=True)
    thumbnail=db.Column(db.String)
    # memo_pic = image_attachment('MemoPictures')