from models.db import db,Base

class UserCalendarModel(db.Model,Base):
    __tablename__ = "calendar"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=True)
    title = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    additional_info = db.Column(db.Text)