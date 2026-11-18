"""Tests for transaction history."""


def test_list_transactions_requires_auth(client):
    response = client.get("/api/transactions")
    assert response.status_code == 401


def test_list_transactions_authenticated(client, auth_headers):
    response = client.get("/api/transactions", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "transactions" in data
    assert "total" in data


def test_list_payments(client, auth_headers):
    response = client.get("/api/transactions/payments", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "payments" in data
