from flask import request, Blueprint
from flask_restful import abort
from repositories.locationRepository import LocationRepository
from middlewares.validation.userLocationValidation import UserLocationSchema
from middlewares.auth import token_required

user_location_bp = Blueprint('userlocation', __name__)
manySchema=UserLocationSchema(many=True)
singleSchema=UserLocationSchema()
locationRepository= LocationRepository()
@user_location_bp.post('')
@token_required
def post():
    
    errors= singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    payload =UserLocationSchema().load(request.json)
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(locationRepository.create(payload))

@user_location_bp.get('')
@token_required
def get():
    result= locationRepository.get_all()
    return manySchema.dump(result)

@user_location_bp.patch('/<int:id>')
@token_required
def patch(id):
    errors= singleSchema.validate(request.get_json(),partial=True)
    if errors:
        return errors, 422
    payload =UserLocationSchema().load(request.get_json(),partial=True)
    result=locationRepository.update(payload,id)
    if not result:
        return "Location Id doesn't exist",404
    return singleSchema.dump(result)

@user_location_bp.delete('/<int:id>')
@token_required
def delete(id):
    result = locationRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)