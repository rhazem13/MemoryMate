from models.db import db


class UserAgenda (db.Model):
    __tablename__ = "agenda"
    id = db.Column(db.Integer, primary_key=True)
    date= db.Column(db.DateTime(timezone=True))
    occasion = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, ForeignKey("user.id"))