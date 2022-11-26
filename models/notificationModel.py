# ...
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

db = SQLAlchemy()


class NotificationModel(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    type = db.String(100)
    created_at = db.Column(db.DateTime(timezone=True),
                        server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))