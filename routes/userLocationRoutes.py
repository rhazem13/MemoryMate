from flask import request, Blueprint
from flask_restful import abort
from repositories.locationRepository import LocationRepository
from middlewares.validation.userLocationValidation import UserLocationSchema
from middlewares.auth import token_required
import json

user_location_bp = Blueprint('userlocation', __name__)
manySchema = UserLocationSchema(many=True)
singleSchema = UserLocationSchema()
locationRepository = LocationRepository()


@user_location_bp.post('')
@token_required
def post():

    errors = singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    payload = UserLocationSchema().load(request.json)
    user_id = request.current_user.id
    payload['user_id'] = user_id
    payload['geom'] = "POINT("+str(payload['lng'])+" "+str(payload['lat'])+")"
    del payload['lat']
    del payload['lng']
    if('id' in payload):
        return "Id field shouldn't be entered", 422
    locationRepository.create(payload)
    return "created waypoint"


@user_location_bp.patch('/<int:id>')
# @token_required
def patch(id):
    errors = singleSchema.validate(request.get_json(), partial=True)
    if errors:
        return errors, 422
    payload = UserLocationSchema().load(request.get_json(), partial=True)
    result = locationRepository.update(payload, id)
    if not result:
        return "Location Id doesn't exist", 404
    return singleSchema.dump(result)


@user_location_bp.delete('/<int:id>')
# @token_required
def delete(id):
    result = locationRepository.delete(id)
    if(result):
        return {"deleted": f"{id}"}
    abort(404)


@user_location_bp.get('')
@token_required
def get_waypoints():
    id = request.current_user.id
    if request.current_user.user_type == "PATIENT":
        result = locationRepository.get_caregivers_location(id)
    else:
        result = locationRepository.get_patients_location(id)
    result_arr = []
    print(result)
    for row in result:
        new_row = {"bio": row.bio, "full_name": row.full_name,
                   "user_id": row.user_id}
        result_arr.append(new_row)
        json_geom = json.loads(row.geom)['coordinates']
        new_row['lat'] = json_geom[0]
        new_row['lng'] = json_geom[1]
    return manySchema.dump(result_arr)


@user_location_bp.get("<int:id>")
@token_required
def getUserLocation(id):
    current_user = request.current_user
    if(current_user.user_type=="PATIENT"):
        result = locationRepository.get_waypointsOfCaregiver(current_user.id, id)
    else:
        result = locationRepository.get_waypointsOfPatient(id, current_user.id)
    json_geom = json.loads(result[0].geom)['coordinates']
    new_result = {"bio":result[0].bio, "full_name":result[0].full_name, "lat":json_geom[0], "lng":json_geom[1]}
    return singleSchema.dump(new_result)
