import backoff
import requests
from hotglue_singer_sdk.target_sdk.client import HotglueSink
from target_cmic.auth import CmicBasicAuthenticator


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


class CmicSink(HotglueSink):

    @property
    def base_url(self):
        return self.config.get("base_url")

    @property
    def authenticator(self):
        return CmicBasicAuthenticator(
            f"{self.config.get("client_id")}||{self.config.get("user_id")}",
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

    def preprocess_record(self, record: dict, context: dict) -> dict:
        return record

    def upsert_record(self, record: dict, context: dict):
        state_updates = dict()
        method = "POST"
        endpoint = self.endpoint
        pk = self.key_properties[0] if self.key_properties else "id"

        if record is not None:
            id = record.pop(pk, None)

            if id:
                method = "PATCH"
                endpoint = f"{endpoint}/{id}"

            response = self.request_api(method, endpoint=endpoint, request_data=record)
            if not id:
                id = response.json().get(self.pk)     

            return id, True, state_updates