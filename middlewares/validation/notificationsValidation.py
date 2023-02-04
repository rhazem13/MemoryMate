from marshmallow import Schema,fields,ValidationError,validates
from repositories.UserRepo import UserRepo

class NotificationBodySchema(Schema):
    data = fields.String(required=True)
    sender = fields.String(required=True)

class NotificationSchema(Schema):
    class Meta:
        fields = ("id","user_id","title","body","created_at","type")
    user_id = fields.Integer(required=True)
    title = fields.String(required=True)
    body = fields.Nested(NotificationBodySchema)
    created_at = fields.DateTime(required=True)
    type = fields.String(required=False)

    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepo.get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")