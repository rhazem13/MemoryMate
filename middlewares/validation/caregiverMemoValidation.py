from marshmallow.validate import Length,OneOf,Regexp
from marshmallow import Schema, fields, validates, ValidationError
from middlewares.validation.userValidation import CreateUserscheme
from middlewares.validation.userMemoryValidation import MemorySchema



class Caregivermemories(Schema):
    memory_id=fields.Int()
    caregiver_id=fields.Int()
    

