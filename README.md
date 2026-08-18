# target-cmic

`target-cmic` is a Singer target for writing data to the [CMiC](https://www.cmicglobal.com/) REST API, built with the Meltano SDK for Singer Targets.

## Installation

```bash
pipx install target-cmic
```

## Configuration

### Accepted Config Options

| Setting    | Required | Description                          |
|------------|----------|--------------------------------------|
| `base_url` | Yes      | CMiC API base URL                    |
| `client_id`| Yes      | CMiC Client ID                       |
| `user_id`  | Yes      | CMiC User ID                         |
| `password` | Yes      | Basic auth password                  |

Example `config.json`:

```json
{
  "base_url": "https://partner-sandbox-api-basic.cmiccloud.com/cmicprtn",
  "client_id": "COMPANY",
  "user_id": "USER",
  "password": "secret"
}
```

### Sinks

The target uses named sinks; each stream must match a registered sink. Records are sent to the CMiC REST API with Basic Auth.

| Stream     | Sink           | Endpoint                      | Key property |
|------------|----------------|-------------------------------|--------------|
| `insurance`| `InsuranceSink`| `/ap-rest-api/rest/1/apinsurance` | `InsVUuid`   |

**Behavior**

- **New records:** POST to `{base_url}{endpoint}`. If the record has no key (`InsVUuid` for insurance), the sink sets it to an empty string so the API returns the created UUID.
- **Existing records:** If the record contains the key property, the target PATCHes `{base_url}{endpoint}/{id}` instead of POSTing.

Example Singer input for the insurance stream:

```json
{"type": "SCHEMA", "stream": "insurance", "schema": {"type": "object", "properties": {}}, "key_properties": ["InsVUuid"]}
{"type": "RECORD", "stream": "insurance", "record": {"InsComplType": "VEN", "InsCompCode": "001", "InsCertNum": "123"}}
{"type": "STATE", "value": {}}
```

This POSTs the record to `{base_url}/ap-rest-api/rest/1/apinsurance`. A record that includes `InsVUuid` is PATCHed to `{base_url}/ap-rest-api/rest/1/apinsurance/{InsVUuid}`.

## Usage

```bash
target-cmic --version
target-cmic --help
tap-xxx | target-cmic --config /path/to/config.json
```

## Development

```bash
pipx install poetry
poetry install
poetry run target-cmic --help
```
