# MemoryMate

A team project exploring memory aids, caregiver reminders, contacts, and location features. This repository contains the Flask backend and experimental machine-learning code.

## Backend structure

- `routes/`: Flask blueprints for users, contacts, memories, calendars, locations, and notifications.
- `models/` and `repositories/`: SQLAlchemy models and data access; Alembic migrations are in `migrations/`.
- PostgreSQL with PostGIS stores relational data and geographic points.
- Redis supports caching and session/socket coordination. Flask-SocketIO and the event emitter support real-time notifications.
- Cloudinary handles photo uploads; Twilio supports verification.

This is a historical prototype, not a healthcare production system. The face-recognition and image-classification experiments have separate native/ML dependencies and are not medical diagnostic tools.

## Historical application setup

The full dependency manifest is retained as a record of the original prototype, not a supported deployment environment. A 2026-10-03 audit reported 164 advisories across 20 pinned packages, including the legacy ML chain. Do not deploy that manifest. The reproducible verification path is the focused backend environment below; its separate dependency audit reported no known findings on that date. That result does not validate ML inference or provider security.

Use a Python 3.10 virtual environment, PostgreSQL with PostGIS, and Redis:

```sh
python -m venv .venv
# Activate .venv for your operating system.
# The historical full manifest requires dependency migration before use.
# Copy .env.example to .env and configure your own services.
flask --app app db upgrade
flask --app app run
```

Enable PostGIS in the target database before running migrations. The legacy ML code additionally imports TensorFlow, face_recognition/dlib, OpenCV, and Pillow; the original requirements do not provide a complete portable ML installation. Full application startup requires these dependencies. Do not use bundled Windows wheels as a substitute for a compatible environment.

## Configuration and authentication

`.env.example` lists configuration names without credentials. `DB_URL` and a fresh random `JWT_SECRET_KEY` of at least 32 characters are required; missing values prevent startup. Cloudinary and Twilio configuration is required by the corresponding services. HTTP endpoints using authentication expect `x-access-token`; the socket decorator uses the `token` header. Signing and verification use the configured key.

Never commit `.env`, user photos, bearer tokens, or service credentials. Credentials exposed in earlier versions must be rotated; cleaning Git history does not revoke them. Existing tokens become invalid when the signing key changes.

## Authorization boundaries

The authenticated caller owns calendars, agendas, notifications, faces, and locations. Contact relationships are created by the patient; relationship IDs cannot be reassigned through a patch. Shared repository queries scope reads, updates, and deletes to the owner. Unauthorized and missing objects return 404; missing/invalid credentials return 401. Ownership fields supplied by a client are rejected.

Memories and their pictures can also be read by explicitly granted caregivers. Only the memory owner can modify them or grant/revoke access, and a grant requires an existing caregiver contact. Contact-based location sharing is separate from memory sharing.

Face images are stored below the application's private `instance/faces/<user>` directory and served through an authenticated owner-only route. Recognition searches that user's directory. Provider uploads accept validated base64 JPG/PNG content, not client-supplied file paths or remote URLs. Tokens expire after one hour; profile patches cannot change identity, credentials, or role.

## Focused backend verification

[Authorization tests](tests/test_authorization.py) exercise the actual Flask routes and SQLAlchemy queries against disposable PostgreSQL/PostGIS persistence. They cover owner/wrong-owner/missing-object behavior across six resources, list isolation, ownership spoofing, caregiver grants/revocation, picture access, private media, and token rejection. Configuration/signing and upload-path tests run alongside them.

```sh
docker run -d --name memorymate-auth-test -p 127.0.0.1:55432:5432 \
  -e POSTGRES_DB=memorymate_auth_test -e POSTGRES_HOST_AUTH_METHOD=trust postgis/postgis:16-3.5
python -m pip install -r requirements-backend-test.txt
export TEST_DATABASE_URL=postgresql://postgres@localhost:55432/memorymate_auth_test
python -m pytest tests -q
```

On PowerShell, set `$env:TEST_DATABASE_URL` instead of `export`. The tests reset only a database with the `memorymate_auth_test` suffix; never point them at application data. The trust-authenticated database above binds to loopback and is for disposable tests only.

[Backend CI](.github/workflows/backend-tests.yml) uses Python 3.12 and a real PostGIS service. It validates these backend/security boundaries, not full application startup, provider integration, native ML inference, or the disabled reminder scheduler. The legacy application's dependency file remains separate from the focused test environment. Public Cloudinary URLs are not a private media access-control mechanism; production use would require a separate private asset delivery design.

## Contribution

Built collaboratively. Hazem Ragab contributed to the backend; the repository history records the work of all contributors. The project is retained as earlier engineering work rather than presented as current employer code.
