
# AI Model API Platform Architecture

## Executive Summary

This repository defines a Django-based platform that exposes locally hosted AI models (via **Ollama**) as authenticated REST APIs. It provides:

* **OpenAI-compatible endpoints** for standard access.
* **Security and usage policy enforcement** via API keys, rate limits, and payload validation.
* **Observability**, logging all requests, responses, and usage metrics.

---

## System Architecture Overview

* Clients call **REST endpoints** compatible with OpenAI APIs.
* Django app:

  * Authenticates requests via API keys.
  * Validates payloads.
  * Proxies requests to **Ollama**.
  * Streams/returns responses.
  * Logs all interactions for usage tracking.
* **PostgreSQL** stores users, API keys, and usage logs.
* **Optional Redis** for rate limiting and caching.
* Deployed in containers behind **Nginx**.

---

## Django Application Components

### 1. User Management

* Uses Django's auth system for admin users.
* Custom `User` model or extension to define roles and quotas.

### 2. API Key System

* Create, rotate, and revoke API keys.
* Store keys as **one-way hashes**; prefixes stored for identification.
* Define scopes and access limits per key.

### 3. Request Handling

* Built on **Django REST Framework (DRF)**.
* Async views for streaming responses.
* Normalized error handling.

### 4. Usage Tracking

* Middleware/service logs request/response metadata:

  * Token counts
  * Latency
  * Status codes
  * Errors

---

## Ollama Integration Layer

* HTTP client connects to local Ollama server (e.g., `http://localhost:11434`).
* Model registry maps logical names to Ollama models.
* Supports streaming with **SSE** and handles timeouts/retries.
* Input/output adapters convert between OpenAI and Ollama formats.

---

## Database Design

**Tables:**

* `users(id, email, is_active, role, created_at)`
* `api_keys(id, user_id FK, key_prefix, key_hash, name, scopes, revoked, created_at, last_used_at)`
* `usage_logs(id, user_id FK, api_key_id FK, endpoint, model, request_id, tokens_in, tokens_out, latency_ms, status_code, error_code, created_at, metadata JSONB)`

---

## Request Flow

1. **Authentication:** Extract API key (`Authorization: Bearer <key>`).
2. **Validation:** DRF serializers enforce schema and quotas/scopes.
3. **Dispatch:** Adapt request to Ollama; handle streaming/non-streaming.
4. **Response:** Normalize to OpenAI schema; propagate errors.
5. **Logging:** Persist usage metrics asynchronously.

---

## API Endpoints

| Method | Endpoint               | Description                        |
| ------ | ---------------------- | ---------------------------------- |
| POST   | `/v1/chat/completions` | OpenAI-compatible chat completions |
| POST   | `/v1/completions`      | OpenAI-compatible completions      |
| POST   | `/v1/embeddings`       | Generate embeddings                |
| GET    | `/v1/models`           | List available models              |

* Streaming supported via `text/event-stream`.

---

## Security

* API keys hashed with **HMAC/Bcrypt/Argon2**; only prefixes stored in plaintext.
* HTTPS termination at Nginx with **HSTS**.
* Rate limiting per key using Redis leaky bucket.
* Payload size limits, schema validation, allowed models list.
* Audit logs, revocation, and restricted CORS.

---

## Scalability & Performance

* Async views with **Gunicorn/Uvicorn workers**.
* Horizontal scaling via containerized deployment.
* Connection pooling, streaming, caching for model lists.
* Separate logging queue using **Celery/Redis** for decoupled I/O.

---

## Deployment Strategy

* **Docker Compose** for Nginx, Django, Postgres, Redis, Ollama.
* CI/CD pipelines for builds and migrations.
* Health checks and environment secrets management.
* Observability:

  * Prometheus exporters
  * Grafana dashboards
  * Structured logs

---

## Technology Stack

* **Backend:** Django, DRF, async views, Python `httpx`.
* **Database:** PostgreSQL, Redis (optional), Celery (optional).
* **Server:** Nginx, Gunicorn/Uvicorn, Docker.
* **AI Models:** Ollama local model server.

---

If you want, I can also create a **visual diagram of this architecture** suitable for embedding in the README, so it’s easier for developers to grasp the workflow at a glance.

Do you want me to make that diagram?
