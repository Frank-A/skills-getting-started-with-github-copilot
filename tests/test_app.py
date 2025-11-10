from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_user@example.com"

    # Ensure the participant is not already signed up (cleanup if needed)
    activities = client.get("/activities").json()
    participants = activities[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Sign up the participant
    signup_resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup_resp.status_code == 200
    assert "Signed up" in signup_resp.json().get("message", "")

    # Verify the participant is now in the activity
    activities_after = client.get("/activities").json()
    assert email in activities_after[activity]["participants"]

    # Unregister the participant
    unregister_resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert unregister_resp.status_code == 200
    assert "Unregistered" in unregister_resp.json().get("message", "")

    # Verify the participant was removed
    activities_final = client.get("/activities").json()
    assert email not in activities_final[activity]["participants"]
