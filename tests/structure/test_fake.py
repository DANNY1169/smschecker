"""Tests for the fake external API functions"""
from app.fake import fake_primary_external_api, fake_secondary_external_api
import uuid


def test_fake_primary_external_api_success():
    """Test successful primary external API call"""
    message = {
        "content": "Hello",
        "phone": "0048600123456",
        "sender": "Alice",
        "api_key": "alice"
    }
    response = fake_primary_external_api(message)
    assert response["api"] == "1"
    assert response["status"] == "SENT"
    assert response["recipient"] == "0048600123456"


def test_fake_primary_external_api_invalid_key():
    """Test primary external API with invalid API key"""
    message = {
        "content": "Hello",
        "phone": "0048600123456",
        "sender": "Alice",
        "api_key": "wrong_key"
    }
    response = fake_primary_external_api(message)
    assert response["api"] == "1"
    assert response["status"] == "403"


def test_fake_secondary_external_api_success():
    """Test successful secondary external API call"""
    message = {
        "body": "Hello",
        "recipient": "0048600123456",
        "sender_name": "Alice",
        "auth_key": "bob"
    }
    response = fake_secondary_external_api(message)
    assert response["api"] == "2"
    assert response["status"] == "OK"
    assert "id" in response
    assert isinstance(response["id"], uuid.UUID)


def test_fake_secondary_external_api_invalid_key():
    """Test secondary external API with invalid auth key"""
    message = {
        "body": "Hello",
        "recipient": "0048600123456",
        "sender_name": "Alice",
        "auth_key": "wrong_key"
    }
    response = fake_secondary_external_api(message)
    assert response["api"] == "2"
    assert response["status"] == "403"


def test_fake_primary_external_api_structure():
    """Test that primary API returns correct structure"""
    message = {
        "content": "Test",
        "phone": "0048600123456",
        "sender": "Alice",
        "api_key": "alice"
    }
    response = fake_primary_external_api(message)
    assert "api" in response
    assert "status" in response
    assert "recipient" in response


def test_fake_secondary_external_api_structure():
    """Test that secondary API returns correct structure"""
    message = {
        "body": "Test",
        "recipient": "0048600123456",
        "sender_name": "Alice",
        "auth_key": "bob"
    }
    response = fake_secondary_external_api(message)
    assert "api" in response
    assert "status" in response
    assert "id" in response

