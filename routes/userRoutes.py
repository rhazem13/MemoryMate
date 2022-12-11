from flask import Flask, request, Blueprint
from flask_restful import Resource, reqparse, abort
from models.user.userModel import User
user_bp = Blueprint('users', __name__)

user_put_args = reqparse.RequestParser()

user_put_args.add_argument("username", type=str, help="username")
user_put_args.add_argument("password", type=str, help="password")

@user_bp.get('/hello')
def get():
    #get user data by id
    return "shaaf"

@user_bp.post('/register')
def post():
    #modify user data by id
    print(request.get_json())
    """ args = user_put_args.parse_args()
    hashed_password = generate_password_hash(args['password'], method='sha256')
    new_user = UserRepo(public_id=str(uuid.uuid4()), name=args['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit() """

def delete(self):
    #delete user by id
    return 1