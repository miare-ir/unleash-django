import logging

from django.conf import settings
from UnleashClient import UnleashClient, _RunState

from unleash_django.constants import UNLEASH_TOKEN, UNLEASH_APP_NAME, UNLEASH_URL


def setting(name, default=None):
    """
    Helper function to get a Django setting by name. If setting doesn't exists
    it will return a default.

    :param name: Name of setting
    :type name: str
    :param default: Value if setting is unfound
    :returns: Setting's value
    """
    return getattr(settings, name, default)


class Client:
    def __init__(self):
        custom_headers = setting('UNLEASH_CUSTOM_HEADERS')
        custom_options = setting('UNLEASH_CUSTOM_OPTIONS')
        custom_strategies = setting('UNLEASH_CUSTOM_STRATEGIES')

        self._url = setting('UNLEASH_URL', UNLEASH_URL)
        self._app_name = setting('UNLEASH_APP_NAME', UNLEASH_APP_NAME)
        self._environment = setting('UNLEASH_ENVIRONMENT', "default")
        self._instance_id = setting('UNLEASH_INSTANCE_ID', "unleash-client-python")
        self._refresh_interval = setting('UNLEASH_INTERVAL_RATE', 15)
        self._refresh_jitter = setting('UNLEASH_REFRESH_JITTER', None)
        self._metrics_interval = setting('UNLEASH_METRICS_INTERVAL', 60)
        self._metrics_jitter = setting('UNLEASH_METRICS_JITTER', None)
        self._disable_metrics = setting('UNLEASH_DISABLE_METRICS', False)
        self._disable_registration = setting('UNLEASH_DISABLE_REGISTRATION', False)
        self._custom_headers = custom_headers or {}
        self._custom_options = custom_options or {}
        self._custom_strategies = custom_strategies or {}
        self._cache_directory = setting('UNLEASH_CACHE_DIRECTORY')
        self._project_name = setting('UNLEASH_PROJECT_NAME')
        self._verbose_log_level = setting('UNLEASH_VERBOSE_LOG_LEVEL', 30)
        self._cache = setting('UNLEASH_CACHE')
        self._token = setting('UNLEASH_API_TOKEN', UNLEASH_TOKEN)
        self._fake_initialize = setting('UNLEASH_FAKE_INITIALIZE', False)

    def _update_custom_header(self):
        auth_header = {'Authorization': self._token, }
        return self._custom_headers.update(auth_header)

    def _set_log_severity(self):
        for logger_name in ['UnleashClient', 'apscheduler.scheduler', 'apscheduler.executors']:
            logging.getLogger(logger_name).setLevel(self._verbose_log_level)

    def connect(self):
        self._update_custom_header()
        self._set_log_severity()

        client = UnleashClient(
            url=self._url,
            app_name=self._app_name,
            custom_headers=self._custom_headers,
            environment=self._environment,
            instance_id=self._instance_id,
            refresh_interval=self._refresh_interval,
            refresh_jitter=self._refresh_jitter,
            metrics_interval=self._metrics_interval,
            metrics_jitter=self._metrics_jitter,
            disable_metrics=self._disable_metrics,
            disable_registration=self._disable_registration,
            custom_options=self._custom_options,
            custom_strategies=self._custom_strategies,
            cache_directory=self._cache_directory,
            project_name=self._project_name,
            verbose_log_level=self._verbose_log_level,
            cache=self._cache,
        )

        if self._fake_initialize:
            client._run_state = _RunState.INITIALIZED
        else:
            client.initialize_client()

        return client
