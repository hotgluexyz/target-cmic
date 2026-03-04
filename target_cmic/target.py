"""CMiC target class."""

from target_hotglue.target import TargetHotglue
from typing import List, Optional, Union, Type
from pathlib import PurePath
from singer_sdk import typing as th
from singer_sdk.sinks import Sink

from target_cmic.sinks import FallbackSync


class TargetCmic(TargetHotglue):
    """Singer target for CMiC."""

    def __init__(
        self,
        config: Optional[Union[dict, PurePath, str, List[Union[PurePath, str]]]] = None,
        parse_env_config: bool = False,
        validate_config: bool = True,
        state: str = None,
    ) -> None:
        self.config_file = config[0] if isinstance(config, list) else config
        super().__init__(config, parse_env_config, validate_config)

    name = "target-cmic"
    SINK_TYPES = [FallbackSync]

    config_jsonschema = th.PropertiesList(
        th.Property(
            "base_url",
            th.StringType,
            required=True,
        ),
        th.Property(
            "username",
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
        return FallbackSync


if __name__ == "__main__":
    TargetCmic.cli()
