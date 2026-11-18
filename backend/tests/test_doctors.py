"""Tests for doctor search and unlock endpoints."""
import pytest


def test_search_doctors_requires_auth(client):
    response = client.get("/api/doctors")
    assert response.status_code == 401


def test_search_doctors_authenticated(client, auth_headers):
    response = client.get("/api/doctors", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "doctors" in data
    assert "total" in data


def test_search_no_results(client, auth_headers):
    """SC-004: No search results returns empty state, not error."""
    response = client.get(
        "/api/doctors?search=zzznomatch12345xyz",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["doctors"] == []


def test_search_by_specialty(client, auth_headers):
    response = client.get(
        "/api/doctors?specialty=Cardiology",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    # All returned doctors should be Cardiology (if any exist in test db)
    for doc in data["doctors"]:
        assert "Cardiology" in doc.get("specialty", "")


def test_search_by_city(client, auth_headers):
    response = client.get(
        "/api/doctors?city=Mumbai",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    for doc in data["doctors"]:
        assert "Mumbai" in doc.get("city", "")


def test_doctor_unlock_insufficient_credits(client, auth_headers):
    """SC-001: Insufficient credits returns 402 and no deduction."""
    # First, search to find a doctor
    search_resp = client.get("/api/doctors", headers=auth_headers)
    doctors = search_resp.json().get("doctors", [])
    if not doctors:
        pytest.skip("No doctors in test DB")

    doctor_id = doctors[0]["id"]

    # New user has 0 credits – should fail with 402
    response = client.post(
        "/api/credits/unlock",
        json={"doctor_id": doctor_id},
        headers=auth_headers,
    )
    assert response.status_code == 402
    assert "Insufficient" in response.json()["detail"]
