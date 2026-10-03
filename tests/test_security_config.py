import importlib
import os
import unittest
import sys
from unittest.mock import patch

from flask import Flask
import jwt
from utils.auth_tokens import encode_token, decode_token


class SecurityConfigTests(unittest.TestCase):
    def test_missing_or_short_signing_key_prevents_startup(self):
        for key in ('', 'short'):
            with self.subTest(key_length=len(key)), patch.dict(os.environ, {'DB_URL': 'sqlite://', 'JWT_SECRET_KEY': key}, clear=True):
                sys.modules.pop('config', None)
                with self.assertRaisesRegex(RuntimeError, 'JWT_SECRET_KEY'):
                    importlib.import_module('config')

    def test_configured_key_preserves_signed_token_flow(self):
        with patch.dict(os.environ, {'DB_URL': 'sqlite://', 'JWT_SECRET_KEY': 'test-only-signing-key-not-for-use-0001'}, clear=True):
            sys.modules.pop('config', None)
            config = importlib.import_module('config').Config
        app = Flask(__name__)
        app.config.from_object(config)
        with app.app_context():
            token = encode_token({'id': 7})
            self.assertEqual(decode_token(token)['id'], 7)
            self.assertIn('exp', decode_token(token))
            app.config['SECRET_KEY'] = 'different-test-only-signing-key-0002'
            with self.assertRaises(jwt.InvalidSignatureError):
                decode_token(token)

    def test_missing_database_configuration_prevents_startup(self):
        sys.modules.pop('config', None)
        with patch.dict(os.environ, {'JWT_SECRET_KEY': 'test-only-signing-key-not-for-use-0001'}, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'DB_URL'):
                importlib.import_module('config')


if __name__ == '__main__':
    unittest.main()
