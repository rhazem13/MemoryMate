from models.UserLocations.userLocationsModel import UserLocationModel
from models.user.userModel import User
from models.UserContacts.userContactsModel import UserContacts
from repositories.repository import Repository
from sqlalchemy import func, distinct
from models.db import db
import json


class LocationRepository(Repository):
    def __init__(self):
        super().__init__(UserLocationModel)

    def get_all(self):
        result = UserLocationModel.query.with_entities(UserLocationModel.additional_info, UserLocationModel.location_name, UserLocationModel.user_id,
                                                       func.ST_AsGeoJSON(func.ST_Envelope(UserLocationModel.geom)).label('geom')).all()
        return result

    def get_waypointsOfCaregiver(self, user_id, contact_id):
        result = UserLocationModel.query.distinct(UserLocationModel.user_id).join(UserContacts, UserContacts.contact_id == UserLocationModel.user_id)\
            .join(User, User.id == UserContacts.contact_id)\
            .with_entities(UserContacts.bio, User.full_name, UserLocationModel.user_id,
                           func.ST_AsGeoJSON(func.ST_Envelope(UserLocationModel.geom)).label('geom'))\
            .filter(UserLocationModel.user_id == contact_id, UserContacts.user_id == user_id, UserContacts.contact_id == contact_id)\
            .all()
        print(result)
        return result

    def get_waypointsOfPatient(self, user_id, contact_id):
        result = UserLocationModel.query.distinct(UserLocationModel.user_id).join(UserContacts, UserContacts.user_id == UserLocationModel.user_id)\
            .join(User, User.id == UserContacts.user_id)\
            .with_entities(UserContacts.bio, User.full_name, UserLocationModel.user_id,
                           func.ST_AsGeoJSON(func.ST_Envelope(UserLocationModel.geom)).label('geom'))\
            .filter(UserLocationModel.user_id == user_id, UserContacts.user_id == user_id, UserContacts.contact_id == contact_id)\
            .all()
        return result

    def get_patients_location(self, id):
        print('adasdasdasdasdasdsa')
        result = UserLocationModel.query.distinct(UserLocationModel.user_id)\
            .join(UserContacts, UserLocationModel.user_id == UserContacts.user_id)\
            .join(User, User.id == UserContacts.user_id)\
            .add_columns(User.full_name, User.id.label('user_id'), UserContacts.bio, func.ST_AsGeoJSON(func.ST_Envelope(UserLocationModel.geom)).label('geom'))\
            .filter(UserContacts.contact_id == id)\
            .group_by(UserLocationModel.user_id, UserLocationModel.id, UserContacts.id, User.id)\
            .order_by(UserLocationModel.user_id, UserLocationModel.id.desc())\
            .all()
        return result

    def get_caregivers_location(self, id):
        result = UserLocationModel.query.distinct(UserLocationModel.user_id)\
            .join(UserContacts, UserLocationModel.user_id == UserContacts.contact_id)\
            .join(User, User.id == UserContacts.contact_id)\
            .add_columns(User.full_name, User.id.label('user_id'), UserContacts.bio, func.ST_AsGeoJSON(func.ST_Envelope(UserLocationModel.geom)).label('geom'))\
            .filter(UserContacts.user_id == id)\
            .group_by(UserLocationModel.user_id, UserLocationModel.id, UserContacts.id, User.id)\
            .order_by(UserLocationModel.user_id, UserLocationModel.id.desc())\
            .all()
        return result

    def create(self, value):
        new_value = self.repoModel(**value)
        db.session.add(new_value)
        db.session.commit()
        db.session.refresh(new_value)
        return new_value
