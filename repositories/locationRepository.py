from models.db import db
from models.UserLocations.userLocationsModel import UserLocationModel

def create(userLocation):
    new_user_location = UserLocationModel(**userLocation)
    db.session.add(new_user_location)
    db.session.commit()
    db.session.refresh(new_user_location)
    return new_user_location

def get_all():
    result = UserLocationModel.query.all()
    return result

def update(new_user_location,id):
    user_location = UserLocationModel.query.get(id)
    if user_location is None:
        return False
    for key, value in new_user_location.items():
        setattr(user_location, key, value)
    db.session.commit()
    return user_location

def delete(id):
    user_location = UserLocationModel.query.get(id)
    if user_location is None:
        return False
    db.session.delete(user_location)
    db.session.commit()
    return True


def get_by_id(id):
    result = UserLocationModel.query.get(id)
    return result