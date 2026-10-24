import os, sys, tempfile
os.environ["DB_PATH"] = os.path.join(tempfile.mkdtemp(), "test.db")
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from app import app

client = app.test_client()


def test_health():
    assert client.get("/health").get_json() == {"status": "ok"}


def test_add_and_list():
    r = client.post("/add", data={"title": "Lunch", "amount": "120", "category": "Food", "date": "2026-10-24"})
    assert r.status_code == 302
    assert b"Lunch" in client.get("/").data


def test_invalid_amount():
    r = client.post("/add", data={"title": "X", "amount": "-5", "category": "Food", "date": "2026-10-24"})
    assert r.status_code == 400
