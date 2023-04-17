import redis
# from flask import current_app
class RedisService:
    redis_client = None

    @staticmethod
    def getClient(current_app):
        if not RedisService.redis_client:
            host = current_app.config['CACHE_REDIS_HOST']
            port = current_app.config['CACHE_REDIS_PORT']
            password = current_app.config['CACHE_REDIS_PASSWORD']
            db = current_app.config['CACHE_REDIS_DB']
            RedisService.redis_client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
        return RedisService.redis_client