from services.caching.CacheDecorator import CacheDecorator
class CacheService:
    cache = CacheDecorator()
    @staticmethod
    def initialize(app) :
        #CacheService.cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
        CacheService.cache = CacheDecorator(app)

    @staticmethod
    def get_instance():
        if CacheService.cache is None:
            raise Exception("Unsupported on fly initialization")
        return CacheService.cache
    
    
