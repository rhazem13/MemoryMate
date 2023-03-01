
from flask import request, jsonify
from functools import wraps
import jwt

def socket_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
            print("we are in token condition")

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token,'secret', algorithms=['HS256'])
            print(data)
        except:
            return jsonify({'message' : 'you are not supposed to be here!'}), 401

        return f(*args, **kwargs)

    return decorator