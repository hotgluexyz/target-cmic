"""CMiC target sink class, which handles writing streams."""

from target_cmic.client import CmicSink


class InsuranceSink(CmicSink):
    """Sink for insurance records."""

    name = "insurance"
    endpoint = f"/ap-rest-api/rest/1/apinsurance"