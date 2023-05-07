from models.user.userModel import User
from repositories.userRepository import UserRepository
from models.user.userModel import User
from flask import request, jsonify
from functools import wraps
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            print('not token')
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, 'secret', algorithms=['HS256'])
            request.current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            print(e)
            return jsonify({'message': 'you are not supposed to be here!'}), 401

        return f(*args, **kwargs)

    return decorated
