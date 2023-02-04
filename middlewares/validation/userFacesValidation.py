from marshmallow import Schema,fields,ValidationError,validates,validate
from repositories.UserRepo import UserRepo
from repositories.facesRepository import FacesRepository
class UserFacesSchema(Schema):
    class Meta:
        fields = ("id","user_id","face_id","name","bio")
    user_id = fields.Integer(required=True)
    face_id = fields.Integer(required=True)
    name = fields.String(required=True)
    bio = fields.String(required=True)

    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepo.get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
    
