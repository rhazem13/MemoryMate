from flask import current_app
from datetime import datetime, timedelta, timezone
import jwt


def encode_token(payload):
    claims = dict(payload)
    claims.setdefault('exp', datetime.now(timezone.utc) + timedelta(hours=1))
    return jwt.encode(claims, current_app.config['SECRET_KEY'], algorithm='HS256')


def decode_token(token):
    claims = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'],
                        options={'require': ['exp', 'id']})
    if type(claims['id']) is not int or claims['id'] <= 0:
        raise jwt.InvalidTokenError('Invalid user identifier')
    return claims
