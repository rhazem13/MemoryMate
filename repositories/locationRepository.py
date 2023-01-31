from flask_restful import fields, marshal_with
from models.db import db
from models.UserLocations.userLocationsModel import UserLocationModel
from sqlalchemy.orm import load_only

resource_fields = {
    'id':fields.Integer,
    'lat':fields.Float,
    'long':fields.Float,
    'user_id':fields.Integer,
    'location_name':fields.String,
    'additional_info':fields.String
}


@marshal_with(resource_fields)
def get_all():
    result = UserLocationModel.query.all()
    return result

@marshal_with(resource_fields)
def get_by_id(id):
    result = UserLocationModel.query.get(id)
    return result

@marshal_with(resource_fields)
def create(userLocation):
    new_user_location = UserLocationModel(**userLocation)
    db.session.add(new_user_location)
    db.session.commit()
    db.session.refresh(new_user_location)
    return new_user_location




@marshal_with(resource_fields)
def update(new_user_location):
    user_location = UserLocationModel.query.get(new_user_location['id'])
    if user_location is None:
        return False
    for key, value in new_user_location.items():
        setattr(user_location, key, value)
    db.session.commit()
    return True


@marshal_with(resource_fields)
def delete(id):
    user_location = UserLocationModel.query.get(id)
    if user_location is None:
        return False
    db.session.delete(user_location)
    db.session.commit()
    return True

