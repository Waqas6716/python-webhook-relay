import hashlib
import hmac
from fastapi.testclient import TestClient
from app.main import app


def test_signed_event_is_accepted():
    body = b'{"type":"order.created"}'
    signature = hmac.new(b"development-secret", body, hashlib.sha256).hexdigest()
    response = TestClient(app).post("/v1/events", content=body, headers={"X-Delivery-Id": "evt-1", "X-Signature": signature})
    assert response.status_code == 202
