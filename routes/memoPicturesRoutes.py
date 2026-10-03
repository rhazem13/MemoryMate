from flask import request, Blueprint, abort
from repositories.memoPicsRepository import MemoryPicsRepository
from repositories.memoRepository import MemoryRepository
from middlewares.validation.memoPicsValiation import MemoryPicSchema
from middlewares.auth import token_required
from models.Memories.memoryPicsModel import MemoPictures
from services.photoservice.photoservice import PhotoService

memories_pics_bp = Blueprint('memory_picture', __name__)
repository = MemoryPicsRepository()
schema = MemoryPicSchema()
many_schema = MemoryPicSchema(many=True)


@memories_pics_bp.post('/memopicsadd')
@token_required
def post():
    errors = schema.validate(request.json)
    if errors:
        return errors, 422
    payload = schema.load(request.json)
    if MemoryRepository().get_by_id(payload['memory_id']) is None:
        abort(404)
    payload['memoPic_path'] = PhotoService.getInstance().addPhoto(
        payload['memoPic_path'], 'memories pictures')
    return schema.dump(repository.create(payload)), 201


@memories_pics_bp.get('/memopicsget/<int:memo_id>')
@token_required
def getmemospics(memo_id):
    if MemoryRepository().get_readable(memo_id) is None:
        abort(404)
    return many_schema.dump(repository.readable_query().filter_by(memory_id=memo_id).all())


@memories_pics_bp.get('/usermemopicsget')
@token_required
def usergetmemospics():
    return many_schema.dump(repository.readable_query().all())


@memories_pics_bp.get('/memopicget/<int:memopic_id>')
@token_required
def getmemo(memopic_id):
    picture = repository.readable_query().filter(MemoPictures.id == memopic_id).first()
    if picture is None:
        abort(404)
    return schema.dump(picture)


@memories_pics_bp.delete('/memopicdel/<int:memopic_id>')
@token_required
def delete(memopic_id):
    if not repository.delete(memopic_id):
        abort(404)
    return {'deleted': memopic_id}
