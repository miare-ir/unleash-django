# unleash-django

This library is a wrapper for Unleash.io's [python](https://docs.getunleash.io/sdks/python_sdk)

It can wrap views and methods to run if only feature is enabled and return a fallback function 
otherwise.

# Setting:
set following values in your settings:

    * UNLEASH_TOKEN = 'your project token',default is 'default:development. unleash-insecure-api-token'
    * UNLEASH_URL = 'the project url', default is 'https://app.unleash-hosted.com/demo/api/'
    * UNLEASH_APP_NAME = 'the app name', default is 'miare'

# wrappers:
### Using view wrapper:

```python
from unleash_django.decorators.view_flag import view_flag


def fallback_func(self):
    """some code goes here"""


@view_flag('feature_name', fallback_func)
def get(self):
    """some code here"""
```

### Using method wrapper:

```python
from unleash_django.decorators.method_flag import method_flag


def fallback_func():
    """ some code goes here """


@method_flag('feature_name', user_id=123)
def method():
    """ some code goes here """
```

if a method feature flag is going to have a user based strategy, `user_id` should be provided

# Methods:

### is_enabled:

```python
from unleash_django.api.method import is_enabled

is_enabled('feature_name', context={'userID': '123'})
```

if feature flag is on, `True` will be returned, otherwise `False` unless `default` is set to 
`True`.

### with_feature_flag:
```python
from unleash_django.api.method import with_feature_flag


def enabled_func():
    """some code goes here"""


def disabled_func():
    """some code goes here"""


with_feature_flag('feature_name', enabled_function=enabled_func, disabled_function=disabled_func)
```

It runs `enabled_function` if feature is on, otherwise `disabled_function` unless `default` 
value is set to `True`

it is possible to pass functions with args and kwargs using tuple, dict or `FlagFunction`
