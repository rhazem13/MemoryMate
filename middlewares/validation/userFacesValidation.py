from marshmallow import Schema,fields,ValidationError,validates,validate
import marshmallow
from repositories.userRepository import UserRepository
class UserFacesSchema(Schema):
    class Meta:
        fields = ("user_id","face_url" ,"name","bio")
    user_id = fields.Integer(required=False)
    # file = marshmallow.fields.Raw(type='file' , required=False)
    name = fields.String(required=True)
    bio = fields.String(required=True)
# "id","user_id","face_url",
    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepository().get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
        if(user.user_type.name!='PATIENT'):
            print(user.user_type.name)
            raise ValidationError("User Type Must Be Patient!")
    
