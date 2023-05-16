from marshmallow import Schema, fields, ValidationError, validates, validate
from repositories.userRepository import UserRepository
from models.UserContacts.relationLevelEnum import ERelationLevel


class UserContactsSchema(Schema):
    class Meta:
        fields = ("id", "user_id", "contact_id", "relation",
                  "bio", "email", "phone", "full_name", "address", "photo_path")
    # user_id = fields.Integer(required=True)
    # contact_id = fields.Integer(required=True)\
    email = fields.Email(required=True)
    relation = fields.String(required=True, validate=validate.OneOf(
        ERelationLevel.__members__.keys()))
    bio = fields.String(required=True)
 
    @validates('email')
    def validate_email(self, email):
        contact = UserRepository().get_by_email(email)
        if(contact == None):
            raise ValidationError("Contact email does Not Exist!")
