from flask import abort, request
from models.db import db


def current_user_id():
    user = getattr(request, "current_user", None)
    if user is None:
        abort(401)
    return user.id

class Repository:
    def __init__(self,repoModel):
        self.repoModel = repoModel
    
    def create(self,value):
        value = dict(value)
        if 'id' in value:
            abort(422)
        if not hasattr(self.repoModel, 'user_id'):
            abort(403)
        value['user_id'] = current_user_id()
        new_value = self.repoModel(**value)
        db.session.add(new_value)
        db.session.commit()
        db.session.refresh(new_value)
        return new_value

    def get_all(self):
        result = self.owned_query().all()
        return result

    def update(self,new_value,id):
        old_value = self.get_by_id(id)
        if old_value is None:
            return False
        if {'id', 'user_id', 'contact_id', 'memory_id', 'caregiver_id'}.intersection(new_value):
            abort(422, description='Ownership and identifiers cannot be changed')
        if not set(new_value).issubset(self.repoModel.__table__.columns.keys()):
            abort(422)
        for key, value in new_value.items():
            setattr(old_value, key, value)
        db.session.commit()
        return old_value

    def delete(self,id):
        old_value = self.get_by_id(id)
        if old_value is None:
            return False
        db.session.delete(old_value)
        db.session.commit()
        return True


    def get_by_id(self,id):
        result = self.owned_query().filter(self.repoModel.id == id).first()
        return result

    def owned_query(self):
        if not hasattr(self.repoModel, 'user_id'):
            abort(403)
        return self.repoModel.query.filter_by(user_id=current_user_id())
