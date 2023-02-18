from flask import request, Blueprint
from services.EventEmitter.event_emitter import EventEmitter
from middlewares.auth import token_required
from repositories.userRepository import UserRepository
from middlewares.validation.userValidation import CreateUserscheme

userScheme = CreateUserscheme(many=True)
userRepository = UserRepository()
caring_bp = Blueprint('caring', __name__)

@caring_bp.get('mypatients')
@token_required
def get():
    # patient 
    result = userRepository.get_patients_by_caregiver_id(request.current_user.id)
    print(result)
    return userScheme.dump(result)