import hashlib
import hmac
import os

from fastapi import FastAPI, Header, HTTPException, Request, status

app = FastAPI(title="Webhook Relay")
_delivered: set[str] = set()
_secret = os.getenv("WEBHOOK_SECRET", "development-secret").encode()


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/v1/events", status_code=status.HTTP_202_ACCEPTED)
async def receive(request: Request, x_delivery_id: str = Header(min_length=1), x_signature: str = Header(min_length=64)):
    body = await request.body()
    expected = hmac.new(_secret, body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, x_signature.removeprefix("sha256=")):
        raise HTTPException(status_code=401, detail="invalid signature")
    if x_delivery_id in _delivered:
        return {"delivery_id": x_delivery_id, "status": "duplicate"}
    _delivered.add(x_delivery_id)
    return {"delivery_id": x_delivery_id, "status": "accepted"}
