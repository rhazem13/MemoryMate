from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base



# from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
