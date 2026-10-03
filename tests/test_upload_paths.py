from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from utils.uploads import image_path


class UploadPathTests(unittest.TestCase):
    def test_user_filename_cannot_escape_the_upload_directory(self):
        with TemporaryDirectory() as directory:
            result = Path(image_path(directory, '../../outside.jpg'))
            self.assertEqual(result.parent, Path(directory).resolve())

    def test_non_image_or_empty_name_is_rejected(self):
        with TemporaryDirectory() as directory:
            for name in ('', '../../config.py', 'payload.exe'):
                with self.subTest(name=name), self.assertRaises(ValueError):
                    image_path(directory, name)


if __name__ == '__main__':
    unittest.main()
