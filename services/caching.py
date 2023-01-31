from flask_caching import Cache
class CacheService:
    cache = Cache()
    @staticmethod
    def initialize(app) :
        #CacheService.cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
        CacheService.cache = Cache(app)

    @staticmethod
    def get_instance():
        if CacheService.cache is None:
            raise Exception("Unsupported on fly initialization")
        return CacheService.cache