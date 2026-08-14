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
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "user_id",
            th.StringType,
            required=True,
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
        ),
    ).to_dict()

    def get_sink_class(self, stream_name: str) -> Type[Sink]:
        for sink_type in self.SINK_TYPES:
            if sink_type.name == stream_name:
                return sink_type

if __name__ == "__main__":
    TargetCmic.cli()
