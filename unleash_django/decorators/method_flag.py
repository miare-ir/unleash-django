from collections.abc import Callable
from functools import wraps

from unleash_django.api.method import is_enabled
from unleash_django.exceptions import FallbackException


def method_flag(feature_name: str, user_id: int = None, custom_context: dict = None,
                fallback_func: Callable = None, default: bool = False):

    def decorator(f):

        def _check_with_context():
            app_context = custom_context or {}
            if user_id is not None:
                app_context.update({"userId": str(user_id)})

            return is_enabled(feature_name, context=app_context, default=default)

        def _return_fallback_func(*args, **kwargs):
            if fallback_func is not None:
                return fallback_func(*args, **kwargs)
            raise FallbackException()

        @wraps(f)
        def decorated(*args, **kwargs):
            if user_id is not None or custom_context is not None:
                enabled = _check_with_context()
            else:
                enabled = is_enabled(feature_name, default=default)
            if enabled:
                return f(*args, **kwargs)
            return _return_fallback_func(*args, **kwargs)
        return decorated
    return decorator
