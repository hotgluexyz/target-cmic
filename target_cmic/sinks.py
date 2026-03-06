"""CMiC target sink class, which handles writing streams."""

from target_cmic.client import CmicSink


class InsuranceSink(CmicSink):
    """Sink for insurance records."""

    name = "insurance"
    endpoint = f"/ap-rest-api/rest/1/apinsurance"
    pk = "InsVUuid"

    def preprocess_record(self, record: dict, context: dict) -> dict:
        if not record.get("id", record.get(self.pk)):
            # add empty pk field, or response of creation will not have the uuid
            record[self.pk] = ""
        return record