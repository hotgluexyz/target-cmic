"""CMiC target authenticators (Basic Auth and OAuth2 client credentials)."""

from __future__ import annotations

import json
from base64 import b64encode
from datetime import datetime
from typing import Any, Mapping

import requests
from hotglue_singer_sdk.target_sdk.auth import OAuthAuthenticator


class CmicBasicAuthenticator:
    """Basic Auth authenticator for CMiC API."""

    def __init__(self, username: str, password: str) -> None:
        token = b64encode(f"{username}:{password}".encode()).decode()
        self._auth_headers = {"Authorization": f"Basic {token}"}

    @property
    def auth_headers(self) -> dict:
        return self._auth_headers


def resolve_token_url(config: Mapping[str, Any]) -> str:
    """Return Entra token URL from config (`token_url` or `tenant_id`)."""
    token_url = config.get("token_url")
    if token_url:
        return token_url
    tenant_id = config.get("tenant_id")
    if not tenant_id:
        raise RuntimeError(
            "tenant_id or token_url is required for OAuth client credentials."
        )
    return f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"


class CmicOAuthAuthenticator(OAuthAuthenticator):
    """Entra client-credentials auth for the CMiC OAuth API host."""

    def __init__(self, target, state=None, auth_endpoint: str | None = None) -> None:
        super().__init__(
            target,
            state or {},
            auth_endpoint=auth_endpoint or resolve_token_url(target._config),
        )

    @property
    def oauth_request_body(self) -> dict:
        client_id = self._config["client_id"]
        return {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": self._config["client_secret"],
            "scope": self._config.get("scope") or f"api://{client_id}/.default",
        }

    def _update_access_token_locally(self) -> None:
        """Mint a client-credentials token and update config.

        Override until hotglue-singer-sdk is bumped (PR #71): the SDK method
        always writes ``refresh_token`` from the token response, which Entra
        client credentials does not return.
        """
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        now = round(datetime.utcnow().timestamp())
        token_response = requests.post(
            self._auth_endpoint,
            data=self.oauth_request_body,
            headers=headers,
            timeout=300,
        )
        try:
            token_response.raise_for_status()
            self.logger.info("OAuth authorization attempt was successful.")
        except Exception as ex:
            self.state.update({"auth_error_response": token_response.text})
            raise RuntimeError(
                f"Failed OAuth login, response was '{token_response.text}'. {ex}"
            ) from ex

        token_json = token_response.json()
        self._config["access_token"] = token_json["access_token"]
        self._config["expires_in"] = int(token_json["expires_in"]) + now

        if self._config_file_path is not None:
            with open(self._config_file_path, "w") as outfile:
                json.dump(self._config, outfile, indent=4)
