from geoalchemy2 import Geometry  # <= not used but must be imported
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, post_load
db = SQLAlchemy()
ma = Marshmallow()
""" from models.user.userModel import User
from UserAgenda.userAgendaModel import UserAgenda
from UserCalendar.userCalendarModel import UserCalendarModel
from UserContacts.userContactsModel import UserContacts
from UserFaces.userfacesModel import UserfacesModel
from UserLocations.userLocationsModel import UserLocationModel """
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base



# from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
