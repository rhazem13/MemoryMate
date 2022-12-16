from models.db import db,Base



class UserAgenda (db.Model,Base):
    __tablename__ = "user_agenda"
    id = db.Column(db.Integer, primary_key=True)
    date_time= db.Column(db.DateTime(timezone=True))
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))