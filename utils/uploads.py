from pathlib import Path
from werkzeug.utils import secure_filename


def image_path(folder, filename):
    safe_name = secure_filename(filename)
    if not safe_name or Path(safe_name).suffix.lower() not in {'.jpg', '.jpeg', '.png'}:
        raise ValueError('A JPG or PNG filename is required')
    directory = Path(folder).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    return str(directory / safe_name)
