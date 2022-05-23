from collections.abc import Callable
from functools import partial

from unleash_django.client import Client
from unleash_django.exceptions import FallbackException
from unleash_django.models import FlagFunction
from unleash_django.validators import validate_func


def is_enabled(feature_name: str, context: dict = None, default: bool = False) -> bool:
    """
    Check if a feature flag is enabled.
    :param default:  if unleash is not available or does not get a valid response from unleash,
    the default value is returned.
    :param feature_name: The name of the feature flag to check.
    :param context: A dictionary of key-value pairs to use as context for the flag.
    :return: True if the flag is enabled, False otherwise.
    """

    def _custom_fallback(the_feature: str, the_context: dict) -> bool:
        return True

    client = Client().connect()
    if default:
        return client.is_enabled(feature_name, context, fallback_function=_custom_fallback)
    return client.is_enabled(feature_name, context=context)


def with_feature_flag(feature_name: str, enabled_function, disabled_function=None,
                      user_id: int = None, custom_context: dict = None, default: bool = False):

    """
    :param feature_name: The name of the feature flag to check.
    :param enabled_function: the function to call if the flag is enabled. it can be a callable,
    FlagFunction(function, args, kwargs), tuple(function followed by args) or a dict(function,
    args, kwargs)
    :param disabled_function: the function to call if the flag is disabled. it can be a callable,
    FlagFunction(function, args, kwargs), tuple(function followed by args) or a dict(keys are:
    function, args, kwargs)
    :param user_id: if the flag will be enabled based on user, the user id to compare should be
    provided.
    :param custom_context: a custom context can be provided based on feature flag strategies.
    :param default: if unleash is not available or does not get a valid response from unleash,
    the default value is considered as returned.
    :return: calls appropriate function based on the flag status.
    """

    context = custom_context or {}

    def parse_list_as_args(given_func):
        return given_func[1:]

    def parse_dict_as_args(given_func):
        return given_func.get('args', None)

    def parse_dict_as_kwargs(given_func):
        return given_func.get('kwargs', None)

    def _process_func(given_func):
        func = None
        the_args = None
        the_kwargs = None

        if isinstance(given_func, Callable):
            return given_func

        if isinstance(given_func, FlagFunction):
            given_func.validate_function()
            func = given_func.function
            the_args = given_func.args
            the_kwargs = given_func.kwargs

        if isinstance(given_func, dict):
            func = given_func.get('function')
            the_args = parse_dict_as_args(given_func)
            the_kwargs = parse_dict_as_kwargs(given_func)

        if isinstance(given_func, (tuple, list)):
            func = given_func[0]
            the_args = parse_list_as_args(given_func)

        validate_func(func)
        if the_args is None and the_kwargs is None:
            the_func = partial(func)
            return the_func()
        elif the_kwargs is None:
            the_func = partial(func, *the_args)
        elif the_args is None:
            the_func = partial(func, **the_kwargs)
        else:
            the_func = partial(func, *the_args, **the_kwargs)

        return the_func

    def _enabled_func():
        the_func = _process_func(enabled_function)
        return the_func()

    def _disabled_func():
        the_func = _process_func(disabled_function)
        return the_func()

    if user_id is not None:
        context.update({"userId": str(user_id)})
    if is_enabled(feature_name, context=context, default=default):
        return _enabled_func()
    else:
        if disabled_function is not None:
            return _disabled_func()
        raise FallbackException()
