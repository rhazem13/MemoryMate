from flask_caching import Cache
from functools import wraps
class CacheDecorator(Cache):
    def __init__(self, app = None, with_jinja2_ext = True, config=None) -> None:
        super().__init__(app, with_jinja2_ext, config)

    def get_cache(self, key_prefix):
        def inner_decorator (f):
            @wraps(f)
            def decorated(*args, **kwargs):
                if self.has(key_prefix):
                    return self.get(key_prefix)
                function_result = f(*args, **kwargs)
                self.set(key_prefix, function_result)
                return function_result
            return decorated
        return inner_decorator

    def update_cache(self, key_prefix):
        def inner_decorator(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                function_result = f(*args, **kwargs)
                self.set(key_prefix, function_result)
                return function_result
            return decorated
        return inner_decorator