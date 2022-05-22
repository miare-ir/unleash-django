from collections.abc import Callable
from functools import wraps

from unleash_django.api.method import is_enabled
from unleash_django.exceptions import FallbackException, UserException


def view_flag(feature_name: str, fallback_func: Callable = None, default: bool = False):

    def decorator(f):

        def _get_user_id(*args):
            try:
                return args[0].request.user.id
            except:
                raise UserException()

        def _return_fallback_func(*args, **kwargs):
            if fallback_func is not None:
                return fallback_func(*args, **kwargs)
            raise FallbackException()

        @wraps(f)
        def decorated(*args, **kwargs):
            user_id = _get_user_id(*args)
            app_context = {"userId": str(user_id)}
            if is_enabled(feature_name, context=app_context, default=default):
                return f(*args, **kwargs)
            return _return_fallback_func(*args, **kwargs)
        return decorated
    return decorator
