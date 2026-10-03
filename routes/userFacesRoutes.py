from pathlib import Path
from flask import request, Blueprint, abort, send_file
from sqlalchemy.exc import SQLAlchemyError
from models.db import db
from repositories.userFacesRepository import UserfacesRepository
from middlewares.validation.userFacesValidation import UserFacesSchema
from middlewares.auth import token_required
from utils.images import save_face, remove_face, face_directory

user_face_bp = Blueprint('userface', __name__)
schema = UserFacesSchema()
repository = UserfacesRepository()


@user_face_bp.post('')
@token_required
def post():
    errors = schema.validate(request.json)
    if errors:
        return errors, 422
    payload = schema.load(request.json)
    filename = save_face(payload['face_url'])
    payload['face_url'] = filename
    try:
        face = repository.create(payload)
    except SQLAlchemyError:
        db.session.rollback()
        remove_face(filename)
        raise
    return schema.dump(face), 201


@user_face_bp.get('')
@token_required
def get():
    return UserFacesSchema(many=True).dump(repository.get_all())


@user_face_bp.patch('/<int:id>')
@token_required
def patch(id):
    face = repository.get_by_id(id)
    if face is None:
        abort(404)
    errors = schema.validate(request.json, partial=True)
    if errors:
        return errors, 422
    payload = schema.load(request.json, partial=True)
    old_filename = face.face_url
    new_filename = None
    if 'face_url' in payload:
        new_filename = save_face(payload['face_url'])
        payload['face_url'] = new_filename
    try:
        result = repository.update(payload, id)
    except SQLAlchemyError:
        db.session.rollback()
        remove_face(new_filename)
        raise
    if new_filename is not None:
        remove_face(old_filename)
    return schema.dump(result)


@user_face_bp.delete('/<int:id>')
@token_required
def delete(id):
    face = repository.get_by_id(id)
    if face is None:
        abort(404)
    filename = face.face_url
    repository.delete(id)
    remove_face(filename)
    return {'deleted': id}


@user_face_bp.get('/<int:id>/image')
@token_required
def image(id):
    face = repository.get_by_id(id)
    if face is None or not isinstance(face.face_url, str):
        abort(404)
    directory = face_directory().resolve()
    path = (directory / face.face_url).resolve()
    if not path.is_relative_to(directory) or not path.is_file():
        abort(404)
    return send_file(path)
