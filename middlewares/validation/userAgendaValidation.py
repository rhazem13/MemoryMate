from marshmallow import Schema,fields,ValidationError,validates
from marshmallow.validate import Length
from repositories.UserRepo import UserRepo

class UserAgendaSchema(Schema):
    class Meta:
        fields = ("id","title","date_time","user_id")
    title = fields.Str(required=True,validate=Length(1, 254))
    date_time = fields.DateTime(required=True)
    user_id = fields.Int(required=True)

    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepo.get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
        if(user.user_type!='PATIENT'):
            raise ValidationError("User Type Must Be Patient!")