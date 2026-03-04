from target_hotglue.client import HotglueSink
from singer_sdk.plugin_base import PluginBase
from typing import Dict, List, Optional
from base64 import b64encode
import backoff
import requests


def giveup(exc):
    return (
        exc.response is not None
        and 400 <= exc.response.status_code < 500
        and exc.response.status_code != 429
    )


def on_giveup(details):
    if len(details["args"]) == 2:
        url, params = details["args"]
    else:
        url = details["args"]
        params = {}

    raise Exception(
        "Giving up on request after {} tries with url {} and params {}".format(
            details["tries"], url, params
        )
    )


class CmicBasicAuthenticator:
    """Basic Auth authenticator for CMiC API."""

    def __init__(self, username: str, password: str) -> None:
        token = b64encode(f"{username}:{password}".encode()).decode()
        self._auth_headers = {"Authorization": f"Basic {token}"}

    @property
    def auth_headers(self) -> dict:
        return self._auth_headers


class CmicSink(HotglueSink):

    def __init__(
        self,
        target: PluginBase,
        stream_name: str,
        schema: Dict,
        key_properties: Optional[List[str]],
    ) -> None:
        self._target = target
        super().__init__(target, stream_name, schema, key_properties)

    @property
    def base_url(self):
        return self.config.get("base_url")

    @property
    def authenticator(self):
        return CmicBasicAuthenticator(
            self.config.get("username"),
            self.config.get("password"),
        )

    @property
    def http_headers(self) -> dict:
        headers = {}
        headers.update(self.authenticator.auth_headers or {})
        return headers

    @backoff.on_exception(
        backoff.constant,
        (requests.exceptions.RequestException, requests.exceptions.HTTPError),
        max_tries=5,
        jitter=None,
        giveup=giveup,
        on_giveup=on_giveup,
        interval=10,
    )
    def request_api(self, method, endpoint, request_data=None):
        return super().request_api(method, endpoint=endpoint, request_data=request_data)
