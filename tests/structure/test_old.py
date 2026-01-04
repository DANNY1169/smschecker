"""Tests for the old SMS API implementation structure"""
import pytest

from app import errors
from app.old import sms_primary_api, sms_secondary_api


def test_old_primary_api_function_exists():
    """Test that sms_primary_api function exists"""
    assert callable(sms_primary_api)


def test_old_secondary_api_function_exists():
    """Test that sms_secondary_api function exists"""
    assert callable(sms_secondary_api)


def test_old_primary_api_returns_tuple():
    """Test that sms_primary_api returns a tuple"""
    success, response = sms_primary_api("Hello", "600123456", "PL")
    assert isinstance(success, bool)
    assert isinstance(response, dict)


def test_old_secondary_api_returns_tuple():
    """Test that sms_secondary_api returns a tuple"""
    success, response = sms_secondary_api("Hello", "600123456", "PL")
    assert isinstance(success, bool)
    assert isinstance(response, dict)


def test_old_primary_api_validation_country_code():
    """Test old primary API country code validation"""
    with pytest.raises(errors.InvalidCountryException):
        sms_primary_api("Hello", "600123456", "INVALID")


def test_old_primary_api_validation_phone():
    """Test old primary API phone number validation"""
    with pytest.raises(errors.InvalidPhoneNumber):
        sms_primary_api("Hello", "abc123", "PL")


def test_old_primary_api_validation_content():
    """Test old primary API content length validation"""
    with pytest.raises(errors.InvalidContentLength):
        sms_primary_api("A" * 71, "600123456", "PL")


def test_old_secondary_api_validation_country_code():
    """Test old secondary API country code validation"""
    with pytest.raises(errors.InvalidCountryException):
        sms_secondary_api("Hello", "600123456", "INVALID")


def test_old_secondary_api_validation_phone():
    """Test old secondary API phone number validation"""
    with pytest.raises(errors.InvalidPhoneNumber):
        sms_secondary_api("Hello", "abc123", "PL")


def test_old_secondary_api_validation_content():
    """Test old secondary API content length validation"""
    with pytest.raises(errors.InvalidContentLength):
        sms_secondary_api("A" * 161, "600123456", "PL")


def test_old_primary_api_payload_structure():
    """Test that old primary API uses correct payload structure"""
    # This is tested indirectly through the fake API
    success, response = sms_primary_api("Hello", "600123456", "PL")
    assert success is True
    assert "recipient" in response


def test_old_secondary_api_payload_structure():
    """Test that old secondary API uses correct payload structure"""
    # This is tested indirectly through the fake API
    success, response = sms_secondary_api("Hello", "600123456", "PL")
    assert success is True
    assert "status" in response


def test_old_primary_api_content_limit():
    """Test old primary API with exactly 70 characters"""
    content = "A" * 70
    success, response = sms_primary_api(content, "600123456", "PL")
    assert success is True


def test_old_secondary_api_content_limit():
    """Test old secondary API with exactly 160 characters"""
    content = "A" * 160
    success, response = sms_secondary_api(content, "600123456", "PL")
    assert success is True

