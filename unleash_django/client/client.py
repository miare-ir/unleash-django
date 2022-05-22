import os
from typing import Optional

from UnleashClient import UnleashClient, BaseCache

from unleash_django.constants import UNLEASH_TOKEN, UNLEASH_APP_NAME, UNLEASH_URL


class Client:

    def __init__(self,
                 environment: str = "default",
                 instance_id: str = "unleash-client-python",
                 refresh_interval: int = 15,
                 refresh_jitter: Optional[int] = None,
                 metrics_interval: int = 60,
                 metrics_jitter: Optional[int] = None,
                 disable_metrics: bool = False,
                 disable_registration: bool = False,
                 custom_headers: Optional[dict] = None,
                 custom_options: Optional[dict] = None,
                 custom_strategies: Optional[dict] = None,
                 cache_directory: Optional[str] = None,
                 project_name: str = None,
                 verbose_log_level: int = 30,
                 cache: Optional[BaseCache] = None):

        self._url = os.environ.get('UNLEASH_URL', UNLEASH_URL)
        self._app_name = os.environ.get('UNLEASH_APP_NAME', UNLEASH_APP_NAME)
        self._environment = environment
        self._instance_id = instance_id
        self._refresh_interval = refresh_interval
        self._refresh_jitter = int(refresh_jitter) if refresh_jitter is not None else None
        self._metrics_interval = metrics_interval
        self._metrics_jitter = int(metrics_jitter) if metrics_jitter is not None else None
        self._disable_metrics = disable_metrics
        self._disable_registration = disable_registration
        self._custom_headers = custom_headers or {}
        self._custom_options = custom_options or {}
        self._custom_strategies = custom_strategies or {}
        self._cache_directory = cache_directory
        self._project_name = project_name
        self._verbose_log_level = verbose_log_level
        self._cache = cache
        self._token = os.environ.get('UNLEASH_API_TOKEN', UNLEASH_TOKEN)

    def _update_custom_header(self):
        auth_header = {'Authorization': self._token, }
        return self._custom_headers.update(auth_header)

    def connect(self):
        self._update_custom_header()
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

        client.initialize_client()
        return client
