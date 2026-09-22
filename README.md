# target-cmic

`target-cmic` is a Singer target for writing data to the [CMiC](https://www.cmicglobal.com/) REST API, built with [hotglue-singer-sdk](https://github.com/hotgluexyz/HotglueSingerSDK).

## Installation

```bash
pipx install target-cmic
```

## Configuration

Auth mode is selected from config: if `client_secret` is set, the target uses OAuth client credentials; otherwise Basic Auth.

CMiC Cloud uses separate API hosts for Basic vs OAuth. Use the host that matches your auth mode. See CMiC's [Cloud Web APP and API URLs](https://developers.cmicglobal.com/v1/docs/cloud-api-server-urls).

| Setting | Required | Default | Description |
| ------- | -------- | ------- | ----------- |
| `base_url` | yes | — | CMiC API base URL, without a trailing slash (Basic or OAuth host). |
| `client_id` | yes | — | CMiC Client ID (Basic) or Entra application (client) ID (OAuth). |
| `user_id` | Basic | — | CMiC User ID (Basic Auth). |
| `password` | Basic | — | Account password (Basic Auth). |
| `client_secret` | OAuth | — | Entra client secret. |
| `tenant_id` | OAuth* | — | Entra directory (tenant) ID. |
| `token_url` | OAuth* | `https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token` | Entra token endpoint. Built from `tenant_id` when omitted. |
| `scope` | no | `api://{client_id}/.default` | OAuth scope for client credentials. |

\* OAuth requires `client_secret` plus either `tenant_id` or `token_url`.

### Example Basic Auth `config.json`

```json
{
  "base_url": "https://atlas-api.cmiccloud.com/cmicprod",
  "client_id": "Client_ID",
  "user_id": "User_ID",
  "password": "YOUR_PASSWORD"
}
```

### Example OAuth `config.json`

```json
{
  "base_url": "https://atlas-api-oauth.cmiccloud.com/cmicprod",
  "client_id": "ENTRA_APPLICATION_CLIENT_ID",
  "client_secret": "ENTRA_CLIENT_SECRET",
  "tenant_id": "ENTRA_TENANT_ID"
}
```

### Sinks

The target uses named sinks; each stream must match a registered sink. Records are sent to the CMiC REST API with Basic or OAuth auth.

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
