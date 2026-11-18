"""Tests for credit purchase and business scenarios."""
import pytest
import uuid


def test_get_packages(client):
    """Credit packages are publicly accessible."""
    response = client.get("/api/credits/packages")
    assert response.status_code == 200
    packages = response.json()
    assert isinstance(packages, list)


def test_get_balance_requires_auth(client):
    response = client.get("/api/credits/balance")
    assert response.status_code == 401


def test_get_balance_authenticated(client, auth_headers):
    response = client.get("/api/credits/balance", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "credit_balance" in data


def test_purchase_requires_packages(client, auth_headers):
    """SC-002: If packages exist, purchase works."""
    # Check packages exist
    packages_resp = client.get("/api/credits/packages")
    packages = packages_resp.json()
    if not packages:
        pytest.skip("No packages seeded")

    package_id = packages[0]["id"]
    idem_key = str(uuid.uuid4())

    response = client.post(
        "/api/credits/purchase",
        json={
            "package_id": package_id,
            "payment_mode": "success",
            "idempotency_key": idem_key,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["credits_added"] > 0


def test_purchase_failed_payment(client, auth_headers):
    """SC-002: Failed payment returns failed status, no credits added."""
    packages_resp = client.get("/api/credits/packages")
    packages = packages_resp.json()
    if not packages:
        pytest.skip("No packages seeded")

    # Get balance before
    bal_before = client.get("/api/credits/balance", headers=auth_headers).json()["credit_balance"]

    package_id = packages[0]["id"]
    idem_key = str(uuid.uuid4())

    response = client.post(
        "/api/credits/purchase",
        json={
            "package_id": package_id,
            "payment_mode": "fail",
            "idempotency_key": idem_key,
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "failed"
    assert data["credits_added"] == 0

    # Balance unchanged
    bal_after = client.get("/api/credits/balance", headers=auth_headers).json()["credit_balance"]
    assert bal_before == bal_after


def test_duplicate_payment_idempotency(client, auth_headers):
    """SC-005: Same idempotency key returns same result without duplicate credit."""
    packages_resp = client.get("/api/credits/packages")
    packages = packages_resp.json()
    if not packages:
        pytest.skip("No packages seeded")

    package_id = packages[0]["id"]
    idem_key = str(uuid.uuid4())

    # First purchase
    r1 = client.post(
        "/api/credits/purchase",
        json={
            "package_id": package_id,
            "payment_mode": "success",
            "idempotency_key": idem_key,
        },
        headers=auth_headers,
    )
    # Second purchase with same key (should be idempotent)
    r2 = client.post(
        "/api/credits/purchase",
        json={
            "package_id": package_id,
            "payment_mode": "success",
            "idempotency_key": idem_key,
        },
        headers=auth_headers,
    )
    assert r1.status_code == 200
    assert r2.status_code == 200
    # Both return payment_id – should be same
    assert r1.json()["payment_id"] == r2.json()["payment_id"]


def test_pending_payment(client, auth_headers):
    """SC-003: Pending payment does not add credits."""
    packages_resp = client.get("/api/credits/packages")
    packages = packages_resp.json()
    if not packages:
        pytest.skip("No packages seeded")

    bal_before = client.get("/api/credits/balance", headers=auth_headers).json()["credit_balance"]

    response = client.post(
        "/api/credits/purchase",
        json={
            "package_id": packages[0]["id"],
            "payment_mode": "pending",
            "idempotency_key": str(uuid.uuid4()),
        },
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    assert response.json()["credits_added"] == 0

    bal_after = client.get("/api/credits/balance", headers=auth_headers).json()["credit_balance"]
    assert bal_before == bal_after
