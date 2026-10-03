# MemoryMate

A team project exploring memory aids, caregiver reminders, contacts, and location features. This repository contains the Flask backend and experimental machine-learning code.

## Backend structure

- `routes/`: Flask blueprints for users, contacts, memories, calendars, locations, and notifications.
- `models/` and `repositories/`: SQLAlchemy models and data access; Alembic migrations are in `migrations/`.
- PostgreSQL with PostGIS stores relational data and geographic points.
- Redis supports caching and session/socket coordination. Flask-SocketIO and the event emitter support real-time notifications.
- Cloudinary handles photo uploads; Twilio supports verification.

This is a historical prototype, not a production-ready healthcare application. The face-recognition and image-classification experiments have separate native/ML dependencies and are not medical diagnostic tools.

## Local setup

Use a Python 3.10 virtual environment, PostgreSQL with PostGIS, and Redis:

```sh
python -m venv .venv
# Activate .venv for your operating system.
python -m pip install -r requirements.txt
# Copy .env.example to .env and configure your own services.
flask --app app db upgrade
flask --app app run
```

Enable PostGIS in the target database before running migrations. The legacy ML code additionally imports TensorFlow, face_recognition/dlib, OpenCV, and Pillow; the original requirements do not provide a complete portable ML installation. Full application startup requires these dependencies. Do not use bundled Windows wheels as a substitute for a compatible environment.

## Configuration and authentication

`.env.example` lists configuration names without credentials. `DB_URL` and a fresh random `JWT_SECRET_KEY` of at least 32 characters are required; missing values prevent startup. Cloudinary and Twilio configuration is required by the corresponding services. HTTP endpoints using authentication expect `x-access-token`; the socket decorator uses the `token` header. Signing and verification use the configured key.

Never commit `.env`, user photos, bearer tokens, or service credentials. Credentials exposed in earlier versions must be rotated; cleaning Git history does not revoke them. Existing tokens become invalid when the signing key changes.

## Verification

The focused configuration and signing checks need Flask and PyJWT:

```sh
python -m unittest discover -s tests
python -m compileall -q config.py middlewares routes services utils
```

## Contribution

Built collaboratively. Hazem Ragab contributed to the backend; the repository history records the work of all contributors. The project is retained as earlier engineering work rather than presented as current employer code.
