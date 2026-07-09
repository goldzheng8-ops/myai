import importlib
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv(
        "DATABASE_URL",
        "postgresql+psycopg://aiuser:aipassword@127.0.0.1:5432/ai_space",
    )

    import app.db.database as db_module
    import app.main as main_module

    importlib.reload(db_module)
    importlib.reload(main_module)

    with TestClient(main_module.app) as test_client:
        yield test_client


def test_fetch_and_list_news(client, monkeypatch):
    import app.api.news as news_api

    async def fake_get_latest_news():
        return {
            "title": "Test title",
            "url": "https://example.com",
            "source": "hackernews",
        }

    monkeypatch.setattr(news_api, "get_latest_news", fake_get_latest_news)

    fetch_response = client.get("/news/fetch")
    assert fetch_response.status_code == 200
    assert fetch_response.json()["title"] == "Test title"

    list_response = client.get("/news/list")
    assert list_response.status_code == 200
    payload = list_response.json()
    assert len(payload) == 1
    assert payload[0]["title"] == "Test title"
    assert payload[0]["url"] == "https://example.com"
    assert payload[0]["source"] == "hackernews"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q", "-s"]))