from marshmallow import Schema,fields,ValidationError,validates,validate
from repositories.UserRepo import UserRepo
from models.UserContacts.relationLevelEnum  import ERelationLevel
class UserContactsSchema(Schema):
    class Meta:
        fields = ("id","user_id","contact_id","relation","bio")
    user_id = fields.Integer(required=True)
    contact_id = fields.Integer(required=True)
    relation = fields.String(required=True,validate=validate.OneOf(ERelationLevel.__members__.keys()))
    bio = fields.String(required=True)

    @validates('user_id')
    def validate_user_id(self, user_id):
        user=UserRepo.get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
    
    @validates('contact_id')
    def validate_contact_id(self, contact_id):
        contact= UserRepo.get_by_id(contact_id)
        if(contact==None):
            raise ValidationError("Contact Id does Not Exist!")