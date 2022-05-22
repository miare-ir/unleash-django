from collections.abc import Callable
from functools import wraps

from api.method import is_enabled
from exceptions import FallbackException, UserException


def view_flag(feature_name: str, fallback_func: Callable = None, default: bool = False):

    def decorator(f):

        def _check_args_length(args):
            if len(args) == 0:
                raise TypeError('arg with request is required')

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
            _check_args_length(*args)
            user_id = _get_user_id(*args)
            app_context = {"userId": str(user_id)}
            if is_enabled(feature_name, context=app_context, default=default):
                return f(*args, **kwargs)
            return _return_fallback_func(*args, **kwargs)
        return decorated
    return decorator
