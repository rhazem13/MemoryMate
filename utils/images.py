import base64
import binascii
from io import BytesIO
from pathlib import Path
from uuid import uuid4
from flask import abort, current_app
from PIL import Image, UnidentifiedImageError
from repositories.repository import current_user_id

MAX_IMAGE_BYTES = 5 * 1024 * 1024


def decode_image(value):
    if not isinstance(value, str) or len(value) > MAX_IMAGE_BYTES * 4 // 3 + 256:
        abort(422, description='Image must be base64 encoded and at most 5 MiB')
    encoded = value.split(',', 1)[-1]
    try:
        data = base64.b64decode(encoded, validate=True)
        if len(data) > MAX_IMAGE_BYTES:
            abort(422)
        with Image.open(BytesIO(data)) as image:
            if image.format not in {'JPEG', 'PNG'}:
                abort(422)
            image.verify()
    except (binascii.Error, ValueError, UnidentifiedImageError, OSError, Image.DecompressionBombError):
        abort(422, description='A valid JPG or PNG image is required')
    return data


def face_directory():
    directory = Path(current_app.instance_path) / 'faces' / str(current_user_id())
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_face(value):
    data = decode_image(value)
    path = face_directory() / (uuid4().hex + '.jpg')
    with Image.open(BytesIO(data)) as image:
        image.convert('RGB').save(path, format='JPEG')
    return path.name
