"""Tests for the Primary SMS API Provider"""
import pytest

from app import errors
from app.new.providers import PrimarySmsApiProvider


def test_primary_provider_instantiation():
    """Test that PrimarySmsApiProvider can be instantiated"""
    provider = PrimarySmsApiProvider()
    assert isinstance(provider, PrimarySmsApiProvider)


def test_primary_provider_send_success():
    """Test successful send operation"""
    provider = PrimarySmsApiProvider()
    success, response = provider.set_recipient(600123456).set_content("Hello").send()
    assert success is True
    assert response["status"] == "SENT"
    assert response["recipient"] == "0048600123456"


def test_primary_provider_validate_recipient_valid():
    """Test recipient validation with valid input"""
    provider = PrimarySmsApiProvider()
    # Should not raise exception
    provider.set_recipient(600123456, "PL")
    assert provider.recipient == "0048600123456"


def test_primary_provider_validate_recipient_invalid_country():
    """Test recipient validation with invalid country code"""
    provider = PrimarySmsApiProvider()
    with pytest.raises(errors.InvalidCountryException):
        provider.set_recipient(600123456, "XX")


def test_primary_provider_validate_recipient_invalid_phone():
    """Test recipient validation with invalid phone number"""
    provider = PrimarySmsApiProvider()
    with pytest.raises(errors.InvalidPhoneNumber):
        provider.set_recipient("600-123-456")


def test_primary_provider_validate_content_valid():
    """Test content validation with valid input"""
    provider = PrimarySmsApiProvider()
    # Should not raise exception
    provider.set_content("Hello World")
    assert provider.content == "Hello World"


def test_primary_provider_validate_content_too_long():
    """Test content validation with content too long"""
    provider = PrimarySmsApiProvider()
    long_content = "A" * 71
    with pytest.raises(errors.InvalidContentLength):
        provider.set_content(long_content)


def test_primary_provider_validate_content_max_length():
    """Test content validation with maximum allowed length"""
    provider = PrimarySmsApiProvider()
    max_content = "A" * 70
    provider.set_content(max_content)
    assert len(provider.content) == 70


def test_primary_provider_validate_before_sending_missing_content():
    """Test validation before sending when content is missing"""
    provider = PrimarySmsApiProvider()
    provider.set_recipient(600123456)
    with pytest.raises(errors.ContentNotSet):
        provider.send()


def test_primary_provider_validate_before_sending_missing_recipient():
    """Test validation before sending when recipient is missing"""
    provider = PrimarySmsApiProvider()
    provider.set_content("Hello")
    with pytest.raises(errors.RecipientNotSet):
        provider.send()


def test_primary_provider_prepare_payload():
    """Test payload preparation"""
    provider = PrimarySmsApiProvider()
    provider.set_recipient(600123456).set_content("Hello")
    payload = provider._prepare_payload()
    assert payload["content"] == "Hello"
    assert payload["phone"] == "0048600123456"
    assert payload["sender"] == "Alice"
    assert payload["api_key"] == "alice"


def test_primary_provider_process_response_sent():
    """Test response processing for SENT status"""
    provider = PrimarySmsApiProvider()
    response = {"status": "SENT", "recipient": "0048600123456"}
    success, resp = provider._process_response(response)
    assert success is True
    assert resp == response


def test_primary_provider_process_response_not_sent():
    """Test response processing for non-SENT status"""
    provider = PrimarySmsApiProvider()
    response = {"status": "403", "error": "Invalid key"}
    success, resp = provider._process_response(response)
    assert success is False
    assert resp == response


def test_primary_provider_chainable():
    """Test that all methods are chainable"""
    provider = PrimarySmsApiProvider()
    result = provider.set_recipient(600123456).set_content("Hello")
    assert result is provider


def test_primary_provider_different_country():
    """Test provider with different country code"""
    provider = PrimarySmsApiProvider()
    success, response = provider.set_recipient(600123456, "DE").set_content("Hello").send()
    assert success is True
    assert response["recipient"] == "0049600123456"


def test_primary_provider_api_key():
    """Test that API_KEY is set correctly"""
    provider = PrimarySmsApiProvider()
    assert provider.API_KEY == "alice"

