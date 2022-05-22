from collections.abc import Callable
from functools import wraps

from unleash_django.api.method import is_enabled
from unleash_django.exceptions import FallbackException
from unleash_django.validators import validate_user_base_feature


def method_flag(feature_name: str, is_user_based: bool = False, user_id: int = None,
                fallback_func: Callable = None, default: bool = False):

    validate_user_base_feature(is_user_based, user_id)

    def decorator(f):

        def _check_with_context():
            app_context = {"userId": str(user_id)}
            return is_enabled(feature_name, context=app_context, default=default)

        def _return_fallback_func(*args, **kwargs):
            if fallback_func is not None:
                return fallback_func(*args, **kwargs)
            raise FallbackException()

        @wraps(f)
        def decorated(*args, **kwargs):
            if is_user_based:
                enabled = _check_with_context()
            else:
                enabled = is_enabled(feature_name, default=default)
            if enabled:
                return f(*args, **kwargs)
            return _return_fallback_func(*args, **kwargs)
        return decorated
    return decorator
