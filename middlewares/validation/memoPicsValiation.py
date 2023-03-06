from marshmallow.validate import Length,OneOf,Regexp
from marshmallow import Schema, fields, validates, ValidationError
from repositories.userRepository import UserRepository
import datetime
import werkzeug
import json

class MemoryPicSchema(Schema):

    id=fields.Int(dump_only=True)
    memory_id=fields.Int()
    memoPic_path=fields.URL()