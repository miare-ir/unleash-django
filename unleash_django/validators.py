from unleash_django.exceptions import UserException


def validate_user_base_feature(is_user_based: bool, user_id: int):
    if is_user_based and user_id is None:
        raise UserException()


def validate_func(func):
    if not callable(func):
        raise TypeError('function must be callable')


def validate_dict(dictionary):
    if dictionary is None:
        return
    if not isinstance(dictionary, dict):
        raise TypeError('kwargs must be dict')


def validate_list(given_list):
    if given_list is None:
        return
    if not isinstance(given_list, (list, tuple)):
        raise TypeError('args must be list or tuple')
