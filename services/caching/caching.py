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

    def get_cache(key_prefix):
        def inner_decorator (f):
            def decorated(*args, **kwargs):
                if CacheService.cache.has(key_prefix):
                    return CacheService.cache.get(key_prefix)
                return f(*args, **kwargs)
            return decorated
        return inner_decorator

    def update_cache(key_prefix):
        def inner_decorator(f):
            def decorated(*args, **kwargs):
                function_result = f(*args, **kwargs)
                CacheService.cache.set(key_prefix, function_result)
                return function_result
