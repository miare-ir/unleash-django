from collections.abc import Callable

from validators import validate_func, validate_dict, validate_list


class FlagFunction:
    def __init__(self, function: Callable, the_args=None, the_kwargs: dict = None):
        self.function = function
        self.args = the_args
        self.kwargs = the_kwargs

    def validate_function(self):
        validate_func(self.function)
        validate_list(self.args)
        validate_dict(self.kwargs)

