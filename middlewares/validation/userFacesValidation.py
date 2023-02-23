from marshmallow import Schema,fields,ValidationError,validates,validate
from repositories.userRepository import UserRepository
class UserFacesSchema(Schema):
    class Meta:
        fields = ("id","user_id","face_url","name","bio")
    user_id = fields.Integer(required=True)
    face_url = fields.String(required=True)
    name = fields.String(required=True)
    bio = fields.String(required=True)

    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepository().get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
        if(user.user_type!='PATIENT'):
            raise ValidationError("User Type Must Be Patient!")
    
