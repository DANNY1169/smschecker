"""Tests for the old SMS API implementation"""
import pytest

from app import errors
from app.old import sms_primary_api, sms_secondary_api


def test_sms_primary_api_success():
    """Test successful primary API call"""
    success, response = sms_primary_api("Hello", "600123456", "PL")
    assert success is True
    assert response["status"] == "SENT"
    assert response["recipient"] == "0048600123456"


def test_sms_primary_api_invalid_country_code():
    """Test primary API with invalid country code"""
    with pytest.raises(errors.InvalidCountryException):
        sms_primary_api("Hello", "600123456", "XX")


def test_sms_primary_api_invalid_phone_number():
    """Test primary API with invalid phone number"""
    with pytest.raises(errors.InvalidPhoneNumber):
        sms_primary_api("Hello", "600-123-456", "PL")


def test_sms_primary_api_invalid_content_length():
    """Test primary API with content too long"""
    long_content = "A" * 71
    with pytest.raises(errors.InvalidContentLength):
        sms_primary_api(long_content, "600123456", "PL")


def test_sms_primary_api_max_content_length():
    """Test primary API with maximum allowed content length"""
    max_content = "A" * 70
    success, response = sms_primary_api(max_content, "600123456", "PL")
    assert success is True


def test_sms_primary_api_default_country_code():
    """Test primary API with default country code"""
    success, response = sms_primary_api("Hello", "600123456")
    assert success is True
    assert response["recipient"] == "0048600123456"


def test_sms_primary_api_different_country():
    """Test primary API with different country code"""
    success, response = sms_primary_api("Hello", "600123456", "DE")
    assert success is True
    assert response["recipient"] == "0049600123456"


def test_sms_secondary_api_success():
    """Test successful secondary API call"""
    success, response = sms_secondary_api("Hello", "600123456", "PL")
    assert success is True
    assert response["status"] == "OK"
    assert "id" in response


def test_sms_secondary_api_invalid_country_code():
    """Test secondary API with invalid country code"""
    with pytest.raises(errors.InvalidCountryException):
        sms_secondary_api("Hello", "600123456", "XX")


def test_sms_secondary_api_invalid_phone_number():
    """Test secondary API with invalid phone number"""
    with pytest.raises(errors.InvalidPhoneNumber):
        sms_secondary_api("Hello", "600-123-456", "PL")


def test_sms_secondary_api_invalid_content_length():
    """Test secondary API with content too long"""
    long_content = "A" * 161
    with pytest.raises(errors.InvalidContentLength):
        sms_secondary_api(long_content, "600123456", "PL")


def test_sms_secondary_api_max_content_length():
    """Test secondary API with maximum allowed content length"""
    max_content = "A" * 160
    success, response = sms_secondary_api(max_content, "600123456", "PL")
    assert success is True


def test_sms_secondary_api_default_country_code():
    """Test secondary API with default country code"""
    success, response = sms_secondary_api("Hello", "600123456")
    assert success is True
    assert response["status"] == "OK"


def test_sms_secondary_api_different_country():
    """Test secondary API with different country code"""
    success, response = sms_secondary_api("Hello", "600123456", "DE")
    assert success is True
    assert response["status"] == "OK"
    assert "id" in response

