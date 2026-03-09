from base64 import b64encode

class CmicBasicAuthenticator:
    """Basic Auth authenticator for CMiC API."""

    def __init__(self, username: str, password: str) -> None:
        token = b64encode(f"{username}:{password}".encode()).decode()
        self._auth_headers = {"Authorization": f"Basic {token}"}

    @property
    def auth_headers(self) -> dict:
        return self._auth_headers
