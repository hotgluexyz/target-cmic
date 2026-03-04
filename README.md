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
| `username` | Yes      | Basic auth username                  |
| `password` | Yes      | Basic auth password                  |

Example `config.json`:

```json
{
  "base_url": "https://partner-sandbox-api-basic.cmiccloud.com/cmicprtn",
  "username": "COMPANY||USER",
  "password": "secret"
}
```

### FallbackSync

The target uses a single `FallbackSync` sink that accepts **any** stream name and maps it directly to a CMiC REST API endpoint. The stream name becomes the URL path appended to `base_url`.

For example, a Singer input like:

```json
{"type": "SCHEMA", "stream": "ap-rest-api/rest/1/apinsurance", "schema": {"type": "object", "properties": {}}, "key_properties": []}
{"type": "RECORD", "stream": "ap-rest-api/rest/1/apinsurance", "record": {"InsComplType": "VEN", "InsCompCode": "001", "InsCertNum": "123"}}
{"type": "STATE", "value": {}}
```

will POST the record to `{base_url}/ap-rest-api/rest/1/apinsurance` with Basic Auth headers.

If the record contains an `id` field (or whatever is set as the key property), the target will PATCH `{endpoint}/{id}` instead of POST.

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
