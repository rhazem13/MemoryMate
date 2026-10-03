from utils.auth_tokens import decode_token
import os
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
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = decode_token(token)
            request.current_user = User.query.filter_by(id=data['id']).first()
            if request.current_user is None:
                return jsonify({'message': 'Invalid token'}), 401
        except (jwt.InvalidTokenError, KeyError):
            return jsonify({'message': 'you are not supposed to be here!'}), 401

        return f(*args, **kwargs)

    return decorated
