import os


def required_env(name):
    value = os.environ.get(name, '').strip()
    if not value or value in {'change-me', 'REMOVED_SENSITIVE_VALUE'}:
        raise RuntimeError(f'{name} must be configured')
    return value


class Config:
    SECRET_KEY = required_env('JWT_SECRET_KEY')
    if len(SECRET_KEY) < 32:
        raise RuntimeError('JWT_SECRET_KEY must contain at least 32 characters')

    SQLALCHEMY_DATABASE_URI = required_env('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'RedisCache')
    CACHE_REDIS_HOST = os.getenv('CACHE_REDIS_HOST', 'localhost')
    CACHE_REDIS_PORT = int(os.getenv('CACHE_REDIS_PORT', '6379'))
    CACHE_REDIS_DB = int(os.getenv('CACHE_REDIS_DB', '0'))
    CACHE_REDIS_PASSWORD = os.getenv('CACHE_REDIS_PASSWORD') or None
    CACHE_REDIS_URL = os.getenv('CACHE_REDIS_URL') or None
    CACHE_DEFAULT_TIMEOUT = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
