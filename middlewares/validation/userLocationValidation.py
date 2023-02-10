from marshmallow import Schema,fields,ValidationError,validates
from repositories.UserRepo import UserRepo
from models.User.userTypeEnum import EUserType

class UserLocationSchema(Schema):
    class Meta:
        fields = ("id","lat","long","user_id","location_name","additional_info")
    lat = fields.Float(required=True)
    long = fields.Float(required=True)
    user_id = fields.Int(required=True)
    location_name = fields.String(required=True)
    additional_info = fields.String(required=False)

    @validates('user_id')
    def validate_user(self, user_id):
        user=UserRepo.get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
        if(user.user_type!='PATIENT'):
            raise ValidationError("User Type Must Be Patient!")