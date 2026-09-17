"""CMiC target class."""

from typing import Type

from hotglue_singer_sdk import typing as th
from hotglue_singer_sdk.sinks import Sink
from hotglue_singer_sdk.target_sdk.target import TargetHotglue

from target_cmic.sinks import InsuranceSink


class TargetCmic(TargetHotglue):
    """Singer target for CMiC."""

    name = "target-cmic"
    SINK_TYPES = [InsuranceSink]

    config_jsonschema = th.PropertiesList(
        th.Property(
            "base_url",
            th.StringType,
            required=True,
            description="Base URL for the CMiC API",
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            description="CMiC Client ID (Basic) or Entra application (client) id (OAuth)",
        ),
        th.Property(
            "user_id",
            th.StringType,
            description="CMiC User ID (Basic Auth)",
        ),
        th.Property(
            "password",
            th.StringType,
            description="CMiC password (Basic Auth)",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            description="Entra client secret (OAuth)",
        ),
        th.Property(
            "tenant_id",
            th.StringType,
            description="Entra directory (tenant) id (OAuth)",
        ),
        th.Property(
            "token_url",
            th.StringType,
            description="Entra OAuth token URL (OAuth)",
        ),
        th.Property(
            "access_token",
            th.StringType,
            description="OAuth access token",
        ),
        th.Property(
            "scope",
            th.StringType,
            description="OAuth scope; defaults to api://{client_id}/.default",
        ),
    ).to_dict()

    def get_sink_class(self, stream_name: str) -> Type[Sink]:
        for sink_type in self.SINK_TYPES:
            if sink_type.name == stream_name:
                return sink_type

if __name__ == "__main__":
    TargetCmic.cli()
