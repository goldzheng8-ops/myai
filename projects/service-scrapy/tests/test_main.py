from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app.main import app


def test_health_endpoint():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_submit_crawl_task(monkeypatch):
    calls = []

    def fake_runner(payload):
        calls.append(payload)
        return {
            "task_id": payload["task_id"],
            "status": "completed",
            "spider": payload["spider"],
            "message": "ok",
        }

    monkeypatch.setattr("app.main.run_scrapy_job", fake_runner)

    client = TestClient(app)
    response = client.post(
        "/crawl/tasks",
        json={"spider": "example", "url": "https://example.com"},
    )

    assert response.status_code == 202
    body = response.json()
    assert body["status"] == "accepted"
    assert body["payload"]["spider"] == "example"
    assert len(calls) == 1
