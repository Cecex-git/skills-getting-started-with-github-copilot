from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Ensure src is on path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from app import app, activities


client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    # Should contain at least one known activity
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test.user@example.com"

    # Ensure not present initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    rv = client.post(f"/activities/{activity}/signup?email={email}")
    assert rv.status_code == 200
    assert email in activities[activity]["participants"]

    # Attempt duplicate signup should fail
    rv2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert rv2.status_code == 400

    # Unregister
    rv3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert rv3.status_code == 200
    assert email not in activities[activity]["participants"]
