"""HTTP authorization boundaries against real PostgreSQL/PostGIS persistence.

TEST_DATABASE_URL must name a disposable database ending in memorymate_auth_test.
No provider calls or ML inference are required for these focused backend tests.
"""
import os
from datetime import date, datetime, timedelta, timezone
from io import BytesIO
import base64
from pathlib import Path

import pytest
from flask import Flask
from PIL import Image
from sqlalchemy import text
from sqlalchemy.engine import make_url

# Configuration is intentionally synthetic; credentials are never used externally.
os.environ.setdefault('DB_URL', 'sqlite://')
os.environ.setdefault('JWT_SECRET_KEY', 'test-only-signing-key-not-for-use-0001')
os.environ.setdefault('CLOUD_NAME', 'unused-test')
os.environ.setdefault('API_KEY', 'unused-test')
os.environ.setdefault('API_SECRET', 'unused-test')
os.environ.setdefault('TWILIO_ACCOUNT_SID', 'AC' + '0' * 32)
os.environ.setdefault('TWILIO_AUTH_TOKEN', 'unused-test')
os.environ.setdefault('VERIFY_SERVICE_SID', 'VA' + '0' * 32)

from models.db import db
from models.user.userModel import User
from models.UserCalendar.userCalendarModel import UserCalendarModel
from models.UserAgenda.userAgendaModel import UserAgenda
from models.Notifications.notificationsModel import NotificationsModel
from models.UserContacts.userContactsModel import UserContacts
from models.UserLocations.userLocationsModel import UserLocationModel
from models.UserFaces.userfacesModel import UserfacesModel
from models.Memories.userMemoriesModel import MemoryModel
from models.Memories.memoryPicsModel import MemoPictures
from repositories.userRepository import UserRepository
from utils.auth_tokens import encode_token
from utils.images import decode_image, save_face
from routes.userCalendarRoutes import user_calendar_bp
from routes.userAgendaRoutes import user_agenda_bp
from routes.notificationRoutes import notification_bp
from routes.userLocationRoutes import user_location_bp
from routes.userContactsRoutes import user_contacts_bp
from routes.userFacesRoutes import user_face_bp
from routes.memoriesroutes import user_memories_bp
from routes.memoPicturesRoutes import memories_pics_bp
from routes.eventsRoutes import events_bp
from routes.caringRoutes import caring_bp
from routes.userRoutes import user_bp


@pytest.fixture
def app(tmp_path):
    url = os.environ.get('TEST_DATABASE_URL')
    if not url:
        pytest.fail('Set TEST_DATABASE_URL to a disposable PostGIS database')
    if not (make_url(url).database or '').endswith('memorymate_auth_test'):
        pytest.fail('Refusing to reset a database without the memorymate_auth_test suffix')
    app = Flask(__name__, instance_path=str(tmp_path))
    app.config.update(TESTING=True, SECRET_KEY='test-only-signing-key-not-for-use-0001',
                      SQLALCHEMY_DATABASE_URI=url, SQLALCHEMY_TRACK_MODIFICATIONS=False)
    db.init_app(app)
    for blueprint, prefix in [
        (user_calendar_bp, '/usercalendar'), (user_agenda_bp, '/useragenda'),
        (notification_bp, '/notifications'), (user_location_bp, '/userlocation'),
        (user_contacts_bp, '/usercontacts'), (user_face_bp, '/userfaces'),
        (user_memories_bp, '/memories'), (memories_pics_bp, '/memopics'),
        (events_bp, '/events'),
        (caring_bp, '/caring'), (user_bp, '/users'),
    ]:
        app.register_blueprint(blueprint, url_prefix=prefix)
    with app.app_context():
        db.session.execute(text('CREATE EXTENSION IF NOT EXISTS postgis'))
        db.session.commit()
        db.drop_all()
        db.create_all()
        users = [User(id=i, full_name=f'Test user {i}', email=f'user{i}@example.invalid',
                      user_type='CAREGIVER' if i == 3 else 'PATIENT',
                      address='Test address', phone=f'+20100000000{i}') for i in (1, 2, 3)]
        db.session.add_all(users)
        db.session.commit()
        yield app
        db.session.rollback()
        db.drop_all()
        db.session.remove()
        db.engine.dispose()


def headers(user_id):
    return {'x-access-token': encode_token({'id': user_id})}


def png():
    buffer = BytesIO()
    Image.new('RGB', (2, 2)).save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode()


RESOURCES = [
    (UserCalendarModel, '/usercalendar', {'title': 'Calendar', 'date': date(2026, 10, 1)}, {'title': 'Updated'}),
    (UserAgenda, '/useragenda', {'title': 'Agenda', 'start_time': datetime.now(timezone.utc), 'repeat_interval': timedelta(minutes=5)}, {'title': 'Updated'}),
    (NotificationsModel, '/notifications', {'title': 'Notification', 'body': {'data': 'Test', 'sender': 'Test'}}, {'title': 'Updated'}),
    (UserContacts, '/usercontacts', {'contact_id': 3, 'relation': 'close', 'bio': 'Test'}, {'bio': 'Updated'}),
    (UserLocationModel, '/userlocation', {'geom': 'POINT(31 30)'}, {'lat': 30, 'lng': 32}),
    (UserfacesModel, '/userfaces', {'name': 'Test face', 'bio': 'Test', 'face_url': 'not-served'}, {'bio': 'Updated'}),
]


@pytest.mark.parametrize('model,path,values,update', RESOURCES)
def test_update_delete_boundaries(app, model, path, values, update):
    row = model(user_id=1, **values)
    db.session.add(row)
    db.session.commit()
    object_id = row.id
    client = app.test_client()
    for method in ('patch', 'delete'):
        body = {'json': update} if method == 'patch' else {}
        assert getattr(client, method)(f'{path}/{object_id}', **body).status_code == 401
        assert getattr(client, method)(f'{path}/{object_id}', headers=headers(2), **body).status_code == 404
        assert getattr(client, method)(f'{path}/999999', headers=headers(1), **body).status_code == 404
    db.session.expire_all()
    assert db.session.get(model, object_id).user_id == 1
    response = client.patch(f'{path}/{object_id}', headers=headers(1), json=update)
    assert response.status_code == 200, response.json
    transfer = client.patch(f'{path}/{object_id}', headers=headers(1), json={'user_id': 2})
    assert transfer.status_code == 422
    assert client.delete(f'{path}/{object_id}', headers=headers(1)).status_code == 200
    db.session.expire_all()
    assert db.session.get(model, object_id) is None


@pytest.mark.parametrize('model,path,values,update', RESOURCES[:3] + RESOURCES[5:])
def test_lists_only_show_owned_records(app, model, path, values, update):
    db.session.add_all([model(user_id=1, **values), model(user_id=2, **values)])
    db.session.commit()
    client = app.test_client()
    assert client.get(path).status_code == 401
    result = client.get(path, headers=headers(1))
    assert result.status_code == 200
    assert len(result.json) == 1
    assert result.json[0]['user_id'] == 1


@pytest.mark.parametrize('path,payload,model', [
    ('/usercalendar', {'title': 'Calendar', 'date': '2026-10-01'}, UserCalendarModel),
    ('/useragenda', {'title': 'Agenda', 'start_time': '2026-10-01T12:00:00Z', 'repeat_interval': 60}, UserAgenda),
    ('/notifications', {'title': 'Notification', 'body': {'data': 'Test', 'sender': 'Test'}, 'created_at': '2026-10-01T12:00:00Z'}, NotificationsModel),
])
def test_creation_uses_authenticated_owner(app, path, payload, model):
    client = app.test_client()
    assert client.post(path, json=payload).status_code == 401
    assert client.post(path, headers=headers(1), json={**payload, 'user_id': 2}).status_code == 422
    result = client.post(path, headers=headers(1), json=payload)
    assert result.status_code == 200, result.json
    db.session.expire_all()
    assert model.query.one().user_id == 1


def test_memory_sharing_and_picture_boundaries(app):
    memory = MemoryModel(user_id=1, title='Private memory', memo_body='Private body')
    memory.caregivers.append(db.session.get(User, 3))
    db.session.add(memory)
    db.session.commit()
    picture = MemoPictures(memory_id=memory.id, memoPic_path='https://example.invalid/test.jpg')
    db.session.add(picture)
    db.session.commit()
    client = app.test_client()
    for path in (f'/memories/memoget/{memory.id}', f'/memopics/memopicget/{picture.id}',
                 f'/memopics/memopicsget/{memory.id}'):
        assert client.get(path).status_code == 401
        assert client.get(path, headers=headers(2)).status_code == 404
        assert client.get(path, headers=headers(1)).status_code == 200
        assert client.get(path, headers=headers(3)).status_code == 200
    for actor in (2, 3):
        assert client.patch(f'/memories/memopatch/{memory.id}', headers=headers(actor), json={'title': 'Changed'}).status_code == 404
        assert client.delete(f'/memories/memodel/{memory.id}', headers=headers(actor)).status_code == 404
        assert client.delete(f'/memopics/memopicdel/{picture.id}', headers=headers(actor)).status_code == 404
        assert client.post(f'/memories/caregiveradd/{memory.id}', headers=headers(actor), json={'caregivers_ids': [3]}).status_code == 404
        assert client.delete(f'/memories/deletecaregiver/{memory.id}', headers=headers(actor), json={'caregivers_ids': [3]}).status_code == 404
    assert client.patch(f'/memories/memopatch/{memory.id}', headers=headers(1), json={'user_id': 2}).status_code == 422
    assert client.patch(f'/memories/memopatch/{memory.id}', headers=headers(1), json={'title': 'Changed'}).status_code == 200
    # A caregiver cannot upload to a memory they can only read.
    assert client.post('/memopics/memopicsadd', headers=headers(3), json={'memory_id': memory.id, 'memoPic_path': png()}).status_code == 404
    assert client.delete(f'/memopics/memopicdel/{picture.id}', headers=headers(1)).status_code == 200
    assert client.delete(f'/memories/memodel/{memory.id}', headers=headers(1)).status_code == 200


def test_sharing_requires_owner_contact_and_can_be_revoked(app):
    memory = MemoryModel(user_id=1, title='Shareable memory')
    db.session.add(memory)
    db.session.commit()
    client = app.test_client()
    grant = f'/memories/caregiveradd/{memory.id}'
    assert client.post(grant, headers=headers(1), json={'caregivers_ids': [3]}).status_code == 403
    db.session.add(UserContacts(user_id=1, contact_id=3, relation='close', bio='Test'))
    db.session.commit()
    assert client.post(grant, headers=headers(1), json={'caregivers_ids': [3]}).status_code == 200
    assert client.get(f'/memories/memoget/{memory.id}', headers=headers(3)).status_code == 200
    assert client.delete(f'/memories/deletecaregiver/{memory.id}', headers=headers(1), json={'caregivers_ids': [3]}).status_code == 200
    assert client.get(f'/memories/memoget/{memory.id}', headers=headers(3)).status_code == 404


def test_private_media_and_removed_debug_routes(app):
    client = app.test_client()
    assert client.post('/userfaces/test', json={'photo': png(), 'folder': 'arbitrary'}).status_code == 404
    assert client.get('/userfaces/test/1').status_code == 404
    assert client.post('/userfaces', json={'name': 'Face', 'bio': 'Test', 'face_url': png()}).status_code == 401
    response = client.post('/userfaces', headers=headers(1), json={'name': '../../escape', 'bio': 'Test', 'face_url': png()})
    assert response.status_code == 201, response.json
    face = UserfacesModel.query.one()
    assert '/' not in face.face_url and '\\' not in face.face_url
    assert (Path(app.instance_path) / 'faces' / '1' / face.face_url).is_file()
    path = f'/userfaces/{face.id}/image'
    assert client.get(path).status_code == 401
    assert client.get(path, headers=headers(2)).status_code == 404
    assert client.get(path, headers=headers(1)).status_code == 200
    assert client.get('/userfaces', headers=headers(1)).json[0]['face_url'] == path


@pytest.mark.parametrize('value', ['file:///etc/passwd', 'https://example.invalid/image.png', '/private/file.jpg', 'not-base64'])
def test_provider_upload_rejects_paths_and_urls(app, value):
    with app.test_request_context():
        from werkzeug.exceptions import UnprocessableEntity
        with pytest.raises(UnprocessableEntity):
            decode_image(value)


def test_authenticated_event_and_profile_mass_assignment(app):
    client = app.test_client()
    payload = {'title': 'Location', 'created_at': '2026-10-01T12:00:00Z'}
    assert client.post('/events/updateCurrentLocation', json=payload).status_code == 401
    assert client.post('/events/updateCurrentLocation', headers=headers(1), json={**payload, 'user_id': 2}).status_code == 422
    for field in ('id', 'email', 'password', 'user_type'):
        assert client.patch('/users/patchuser', headers=headers(1), json={field: 'forged'}).status_code == 422
    assert client.patch('/users/patchuser', json={'full_name': 'Forged'}).status_code == 401
    assert client.patch('/users/patchuser', headers=headers(1), json={'full_name': 'Updated name'}).status_code == 200
    db.session.expire_all()
    assert db.session.get(User, 1).full_name == 'Updated name'
    assert db.session.get(User, 2).full_name == 'Test user 2'


def test_caregiver_patient_read_does_not_expose_credentials(app):
    patient = db.session.get(User, 1)
    patient.password = 'private-test-hash'
    db.session.add(UserContacts(user_id=1, contact_id=3, relation='close', bio='Test'))
    db.session.commit()
    client = app.test_client()
    assert client.get('/caring/mypatients').status_code == 401
    assert client.get('/caring/mypatients', headers=headers(2)).json == []
    response = client.get('/caring/mypatients', headers=headers(3))
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['email'] == patient.email
    assert 'password' not in response.json[0]
    assert b'private-test-hash' not in response.data


def test_invalid_expired_and_missing_user_tokens(app):
    client = app.test_client()
    for token in ['invalid', encode_token({'id': 999999}),
                  encode_token({'id': 1, 'exp': datetime.now(timezone.utc) - timedelta(seconds=1)}),
                  encode_token({'id': '1'}), encode_token({'id': True})]:
        assert client.get('/usercalendar', headers={'x-access-token': token}).status_code == 401


def test_location_and_contact_sharing_require_relationship(app):
    db.session.add(UserLocationModel(user_id=1, geom='POINT(31 30)'))
    db.session.commit()
    client = app.test_client()
    assert client.get('/userlocation/1', headers=headers(3)).status_code == 404
    db.session.add(UserContacts(user_id=1, contact_id=3, relation='close', bio='Test'))
    db.session.commit()
    assert client.get('/userlocation/1', headers=headers(3)).status_code == 200
    assert client.get('/userlocation/1', headers=headers(2)).status_code == 404
    assert client.get('/usercontacts/caregivers', headers=headers(2)).json == []
    assert len(client.get('/usercontacts/caregivers', headers=headers(1)).json) == 1
    assert len(client.get('/usercontacts/patients', headers=headers(3)).json) == 1
