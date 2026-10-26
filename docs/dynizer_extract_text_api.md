# Dynizer Extract Text API

The **Extract Text API** is a lightweight Go service that wraps [Apache Tika](https://tika.apache.org/)
to extract text and metadata from documents. It is designed to plug into the Dynizer
**pipeline-api** as an extraction worker: it registers itself, receives documents,
forwards them to Tika, and returns the extracted text asynchronously via webhooks.

---

## Architecture

```
                  register (every 30s)
   Extract-Text-API ───────────────────────►  Pipeline-API
        │   ▲                                       │
        │   │  POST /extract (job)                  │
        │   └───────────────────────────────────────┘
        │
        │  POST <webhook> (result)
        └───────────────────────────────────────►  Pipeline-API
        │
        ▼  extract
   Apache Tika (bundled, :9998)
```

1. **Register** — Periodically (default every 30s) the service POSTs its identity,
   capacity, and supported filetypes to pipeline-api's register webhook.
2. **Receive** — Pipeline-api sends documents to `POST /extract`. The request is
   queued and a `202 Accepted` is returned immediately (async processing).
3. **Extract** — A worker dequeues the job and forwards the document to Apache Tika.
4. **Callback** — The extracted text + metadata are POSTed back to the `webhook`
   URL supplied in the original request.

Apache Tika runs **inside the same container** (started by `entrypoint.sh` on port
`9998`), so the service is self-contained.

---

## Endpoints

| Method | Path        | Auth | Description                            |
|--------|-------------|------|----------------------------------------|
| POST   | `/extract`  | Yes  | Submit a document for text extraction  |
| GET    | `/state`    | Yes  | Service state and capacity             |
| GET    | `/healthz`  | No   | Kubernetes-style health check          |
| GET    | `/docs`     | No   | Rendered API documentation             |
| GET    | `/spec`     | No   | OpenAPI 3.0 spec                        |

### Authentication

Protected endpoints require a **bearer token**:

```
Authorization: Bearer <token>
```

A token is valid if it matches any value in `authentication.secrets` **or** any
`register.apis[].secret` in the config. This lets pipeline-api call back into the
service using the same shared secret it was registered with.

---

## `POST /extract`

Submits a single document for extraction. Processing is **asynchronous**: the
service validates the request, enqueues it, and returns `202`. The result is later
delivered to the `webhook` URL.

### Request body

```json
{
  "document": {
    "filetype": "pdf",
    "filetype_config": null,
    "base64": {
      "data": "<base64-encoded document bytes>"
    }
  },
  "webhook": "http://pipeline-api:50052/webhooks/extract_result",
  "remote_id": "doc-12345"
}
```

| Field                      | Required | Description                                                        |
|----------------------------|----------|--------------------------------------------------------------------|
| `document.filetype`        | yes      | File type (e.g. `pdf`, `docx`). Must be a supported type.          |
| `document.base64.data`     | yes      | Base64-encoded document bytes.                                     |
| `document.filetype_config` | no       | Optional per-filetype configuration, passed through.              |
| `webhook`                  | yes      | URL the result is POSTed to when extraction finishes.             |
| `remote_id`                | yes      | Caller's own ID for the document; echoed back in the callback.    |

### Response — `202 Accepted`

```json
{
  "id": "f1c2…",        // server-generated extraction ID
  "status": "QUEUED"
}
```

### Error responses

| Code  | Meaning                                                        |
|-------|----------------------------------------------------------------|
| `400` | Missing/invalid field, or unsupported `filetype`.              |
| `503` | Service unavailable (no capacity / not ready).                 |
| `401` | Missing or invalid bearer token.                               |

---

## Webhook callback (result delivery)

When extraction completes (or fails), the service POSTs the following payload to
the `webhook` URL from the original request. Delivery is retried (up to 15 times)
on transient failure.

```json
{
  "id": "f1c2…",          // same extraction ID returned by /extract
  "remote_id": "doc-12345",
  "status": "SUCCESS",     // QUEUED | RUNNING | FAILED | SUCCESS
  "text": "extracted plain text …",
  "metadata": { "Content-Type": "application/pdf", "...": "..." },
  "error": ""              // populated only on FAILED
}
```

On failure, `status` is `FAILED`, `text`/`metadata` are omitted, and `error`
contains the reason.

---

## `GET /state`

Returns current capacity and configuration. Useful for monitoring.

```json
{
  "endpoint": "http://extract-text-api:9999",
  "process_available": 4,
  "process_queued": 0,
  "supported_filetypes": ["pdf", "docx", "doc", "rtf", "odt", "eml", "msg"],
  "tika_endpoint": "http://localhost:9998"
}
```

| Field                 | Description                                   |
|-----------------------|-----------------------------------------------|
| `endpoint`            | Self-reported callback endpoint (`register.self`). |
| `process_available`   | Free processing slots (`max_routines` − active). |
| `process_queued`      | Jobs currently queued.                        |
| `supported_filetypes` | Filetypes advertised to pipeline-api.         |
| `tika_endpoint`       | Tika REST endpoint in use.                     |

---

## `GET /healthz`

Returns `200` when the service is running correctly, `503` otherwise. No auth.
Suitable as a Docker/Kubernetes liveness/readiness probe.

---

## Registration protocol

Every `cron.register_interval` (default 30s), and immediately after each new
`/extract` request, the service POSTs to each `register.apis[].endpoint`:

```json
{
  "endpoint": "http://extract-text-api:9999",   // = register.self (callback address)
  "process_available": 4,
  "process_queued": 0,
  "memory_available": "16GB",
  "supported_filetypes": ["pdf", "docx", "..."],
  "unregister": false,
  "updated_at": "2026-06-30T08:53:26Z"
}
```

with header `Authorization: Bearer <register.apis[].secret>`.

- **`endpoint`** is the value of `register.self` — the address pipeline-api uses
  to send jobs back. It must be resolvable from the pipeline-api container and must
  match the service's hostname (not `0.0.0.0`).
- A `200` response means registration succeeded. A `404` usually means the wrong
  webhook **path**; a `401/403` means the wrong **secret**.

---

## Configuration

Config is loaded from a YAML file via `--config_uri`
(default in the image: `/etc/extract-text-api-server/config/config.yml`).

```yaml
scheme: http
host: 0.0.0.0          # bind address INSIDE the container — must be 0.0.0.0 in Docker
port: 9999             # listen port

tika:
  endpoint: "http://localhost:9998"   # Tika is bundled in the same container
  timeout: 5m
  max_routines: 4                     # max concurrent extractions

log:
  level: info
  format: text

storage:
  db_dir: /var/lib/extract-text-api/extractDB   # persistent queue dir; "" = in-memory

authentication:
  secrets:
    - "<bearer-token>"                # tokens accepted on this API's endpoints

register:
  self: "http://extract-text-api:9999"          # advertised callback address (service name + port)
  apis:
    - endpoint: "http://pipeline-api:50052/webhooks/extract_register"
      secret: "<pipeline-api-token>"             # shared secret with pipeline-api
  insecure_skip_verify: false

cron:
  register_interval: 30s
  queue_interval: 1s
  webhook_interval: 1s

# supported_filetypes: []   # optional; empty = auto-discover all types Tika supports
```

### Key field notes

| Field                  | Notes                                                                                 |
|------------------------|----------------------------------------------------------------------------------------|
| `host`                 | Bind interface. Use `0.0.0.0` in Docker so other containers can connect. Not the same as `register.self`. |
| `register.self`        | Advertised callback URL → must use the **service/host name**, e.g. `http://extract-text-api:9999`. |
| `register.apis.endpoint` | Pipeline-api webhook. Path is `/webhooks/extract_register`; pipeline-api listens on `50052`. |
| `register.apis.secret` | Shared secret. Use the same value in `authentication.secrets` for inbound callbacks.   |
| `storage.db_dir`       | On-disk queue store (extract + webhook queues). Empty = in-memory (lost on restart). Set a path + mount a volume to survive restarts. |
| `supported_filetypes`  | Restricts advertised types. Empty = auto-discovered from Tika at startup.              |

---

## Docker Compose

The Azure image bundles Tika and the wrapper, so a single service is enough:

```yaml
services:
  extract-text-api:
    image: dynizer.azurecr.io/extract-text-api:main
    container_name: extract-text-api        # must match host in register.self
    restart: unless-stopped
    ports:
      - "9999:9999"
    volumes:
      - ./config/extract-text-api.yml:/etc/extract-text-api-server/config/config.yml:ro
      - extract-text-data:/var/lib/extract-text-api   # persists the queues
    healthcheck:
      test: ["CMD", "curl", "-sf", "http://localhost:9999/healthz"]
      interval: 30s
      timeout: 5s
      retries: 3
    depends_on:
      - pipeline-api

volumes:
  extract-text-data:
```

---

## Supported filetypes

Default advertised set: `pdf`, `docx`, `doc`, `rtf`, `odt`, `eml`, `msg`.

If `supported_filetypes` is empty, the service auto-discovers the full list of
types Apache Tika can parse at startup. Setting the list restricts which types are
advertised to pipeline-api (requests for other types are rejected with `400`).

---

## Troubleshooting

| Symptom                                                | Cause / Fix                                                                 |
|--------------------------------------------------------|------------------------------------------------------------------------------|
| `registering ... failed with status code 404`         | Wrong webhook path — use `/webhooks/extract_register`.                       |
| `registering ... failed with status code 401/403`     | `register.apis.secret` doesn't match what pipeline-api expects.             |
| `http server started on 127.0.0.1:9999`               | `host` is loopback — set `host: 0.0.0.0` so other containers can reach it.   |
| Registration succeeds but no jobs arrive              | `register.self` not resolvable from pipeline-api (wrong service name/port).  |
| Queued jobs lost after restart                         | `storage.db_dir` empty (in-memory) — set a path and mount a volume.          |
