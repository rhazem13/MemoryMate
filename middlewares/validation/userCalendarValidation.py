from marshmallow import Schema,fields,ValidationError,validates
from repositories.UserRepo import UserRepo

class UserCalendarSchema(Schema):
    class Meta:
        fields = ("id","date","title","user_id","additional_info")
    date = fields.Date(required=True)
    title = fields.String(required=True)
    user_id = fields.Int(required=True)
    additional_info = fields.String(required=False)

    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepo.get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
