from collections.abc import Callable
from functools import wraps

from unleash_django.api import method
from unleash_django.exceptions import FallbackException, UserException


def view_flag(feature_name: str, fallback_func: Callable = None, custom_context: dict = None,
              default: bool = False):

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
            app_context = custom_context or {}
            app_context.update({"userId": str(user_id)})
            if method.is_enabled(feature_name, context=app_context, default=default):
                return f(*args, **kwargs)
            return _return_fallback_func(*args, **kwargs)
        return decorated
    return decorator
