from models.UserLocations.userLocationsModel import UserLocationModel
from repositories.repository import Repository
from sqlalchemy import func
from models.db import db
import json
class LocationRepository(Repository):
    def __init__(self):
        super().__init__(UserLocationModel)
    def get_all(self):
        result = UserLocationModel.query.with_entities(UserLocationModel.additional_info,UserLocationModel.location_name,UserLocationModel.user_id,
        func.ST_AsGeoJSON(func.ST_Envelope(UserLocationModel.geom)).label('geom')).all()
        return result
    def get_waypoints(self, id):
        result = UserLocationModel.query.with_entities(UserLocationModel.additional_info,UserLocationModel.location_name,UserLocationModel.user_id,
        func.ST_AsGeoJSON(func.ST_Envelope(UserLocationModel.geom)).label('geom')).filter(UserLocationModel.user_id==id).all()
        print(result)
        return result
    def create(self,value):
        new_value = self.repoModel(**value)
        db.session.add(new_value)
        db.session.commit()
        db.session.refresh(new_value)
        return new_value