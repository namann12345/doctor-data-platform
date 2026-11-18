"""Tests for authentication endpoints."""
import pytest


def test_register_success(client):
    response = client.post("/api/auth/register", json={
        "email": "newuser@test.com",
        "password": "NewUser@1234",
        "full_name": "New User",
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["email"] == "newuser@test.com"
    assert data["credit_balance"] == 0


def test_register_duplicate_email(client):
    # First registration
    client.post("/api/auth/register", json={
        "email": "dup@test.com",
        "password": "Dup@12345",
        "full_name": "Dup User",
    })
    # Second registration same email
    response = client.post("/api/auth/register", json={
        "email": "dup@test.com",
        "password": "Dup@12345",
        "full_name": "Dup User 2",
    })
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_login_success(client):
    client.post("/api/auth/register", json={
        "email": "login@test.com",
        "password": "Login@1234",
        "full_name": "Login User",
    })
    response = client.post("/api/auth/login", data={
        "username": "login@test.com",
        "password": "Login@1234",
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    response = client.post("/api/auth/login", data={
        "username": "nonexistent@test.com",
        "password": "wrong",
    })
    assert response.status_code == 401


def test_get_me_authenticated(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert "email" in data
    assert "credit_balance" in data


def test_get_me_unauthenticated(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_protected_route_without_token(client):
    response = client.get("/api/dashboard")
    assert response.status_code == 401
