# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from httpx import ASGITransport  # <- Required to test FastAPI with httpx.AsyncClient

from src.main import app

client = TestClient(app, base_url="http://testserver")

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


@pytest.mark.asyncio
async def test_async_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
