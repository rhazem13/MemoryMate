from marshmallow import Schema,fields,ValidationError,validates
from marshmallow.validate import Length
from repositories.userRepository import UserRepository

class UserAgendaSchema(Schema):
    class Meta:
        fields = ("id","title","start_time","user_id","repeat_interval")
    title = fields.Str(required=True,validate=Length(1, 254))
    start_time = fields.DateTime(required=True)
    user_id = fields.Int(required=True)
    repeat_interval = fields.TimeDelta(required=True)

    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepository().get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
        if(user.user_type!='PATIENT'):
            raise ValidationError("User Type Must Be Patient!")