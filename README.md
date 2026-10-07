# Webhook Relay

An asynchronous FastAPI webhook receiver that verifies HMAC signatures, deduplicates deliveries, and dispatches events to a configured downstream URL. It is intentionally small enough to run locally but structured around production concerns.

Set `WEBHOOK_SECRET` and optionally `DOWNSTREAM_URL` before starting with `uvicorn app.main:app --reload`.
