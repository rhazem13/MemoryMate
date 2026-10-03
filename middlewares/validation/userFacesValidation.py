from marshmallow import Schema,fields,ValidationError,validates,validate
import marshmallow
from repositories.userRepository import UserRepository
class UserFacesSchema(Schema):
    class Meta:
        fields = ("user_id","face_url" ,"name","bio")
    user_id = fields.Int(dump_only=True)
    # file = marshmallow.fields.Raw(type='file' , required=False)
    name = fields.String(required=True, validate=validate.Length(min=1, max=20))
    bio = fields.String(required=True, validate=validate.Length(max=100))
# "id","user_id","face_url",
    face_url = fields.Function(serialize=lambda obj: f'/userfaces/{obj.id}/image',
                              deserialize=lambda value: value, required=True)
