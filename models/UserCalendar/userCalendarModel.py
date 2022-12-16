from models.db import db

class UserCalendarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=True)
    title = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))