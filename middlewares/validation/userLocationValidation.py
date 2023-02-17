import json
from marshmallow import Schema,fields,ValidationError,validates
from repositories.userRepository import UserRepository
from models.user.userTypeEnum import EUserType
from geoalchemy2.shape import to_shape
from geojson import geometry
from geoalchemy2 import Geometry
import geojson
from shapely.geometry import Polygon
from sqlalchemy import func
from shapely import wkb

class UserLocationSchema(Schema):
    class Meta:
        fields = ("id","geom","user_id","location_name","additional_info")
    geom = fields.Method("get_geom", deserialize="load_geom")
    user_id = fields.Int(required=True)
    location_name = fields.String(required=True)
    additional_info = fields.String(required=False)

    def get_geom(self, obj):
        # print(wkb.loads(bytes(obj.geom)))
        # print(to_shape(obj.geom))
        return json.loads(obj.geom)

    def load_geom(self, obj):
        return obj


    @validates('user_id')
    def validate_user(self, user_id):
        user=UserRepository().get_by_id(user_id)
        if(user==None):
            raise ValidationError("User Id Does Not Exist!")
        if(user.user_type!='PATIENT'):
            raise ValidationError("User Type Must Be Patient!")