from models.db import db

class Repository:
    def __init__(self,repoModel):
        self.repoModel = repoModel
    
    def create(self,value):
        new_value = self.repoModel(**value)
        db.session.add(new_value)
        db.session.commit()
        db.session.refresh(new_value)
        return new_value

    def get_all(self):
        result = self.repoModel.query.all()
        return result

    def update(self,new_value,id):
        old_value = self.repoModel.query.get(id)
        if old_value is None:
            return False
        for key, value in new_value.items():
            setattr(old_value, key, value)
        db.session.commit()
        return old_value

    def delete(self,id):
        old_value = self.repoModel.query.get(id)
        if old_value is None:
            return False
        db.session.delete(old_value)
        db.session.commit()
        return True


    def get_by_id(self,id):
        result = self.repoModel.query.get(id)
        return result