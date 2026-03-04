"""CMiC target sink class, which handles writing streams."""

from target_cmic.client import CmicSink


class FallbackSync(CmicSink):
    """Generic sink that forwards any object to the CMiC REST API."""

    @property
    def endpoint(self):
        if self.stream_name.startswith("/"):
            return self.stream_name
        return f"/{self.stream_name}"

    @property
    def name(self):
        return self.stream_name

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

            self.request_api(method, endpoint=endpoint, request_data=record)

            return id, True, state_updates
