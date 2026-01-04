"""Tests for the Secondary SMS API Provider"""
import pytest

from app import errors
from app.new.providers import SecondarySmsApiProvider


def test_secondary_provider_instantiation():
    """Test that SecondarySmsApiProvider can be instantiated"""
    provider = SecondarySmsApiProvider()
    assert isinstance(provider, SecondarySmsApiProvider)


def test_secondary_provider_send_success():
    """Test successful send operation"""
    provider = SecondarySmsApiProvider()
    success, response = provider.set_recipient(600123456).set_content("Hello").send()
    assert success is True
    assert response["status"] == "OK"
    assert "id" in response


def test_secondary_provider_validate_recipient_valid():
    """Test recipient validation with valid input"""
    provider = SecondarySmsApiProvider()
    # Should not raise exception
    provider.set_recipient(600123456, "PL")
    assert provider.recipient == "0048600123456"


def test_secondary_provider_validate_recipient_invalid_country():
    """Test recipient validation with invalid country code"""
    provider = SecondarySmsApiProvider()
    with pytest.raises(errors.InvalidCountryException):
        provider.set_recipient(600123456, "XX")


def test_secondary_provider_validate_recipient_invalid_phone():
    """Test recipient validation with invalid phone number"""
    provider = SecondarySmsApiProvider()
    with pytest.raises(errors.InvalidPhoneNumber):
        provider.set_recipient("600-123-456")


def test_secondary_provider_validate_content_valid():
    """Test content validation with valid input"""
    provider = SecondarySmsApiProvider()
    # Should not raise exception
    provider.set_content("Hello World")
    assert provider.content == "Hello World"


def test_secondary_provider_validate_content_too_long():
    """Test content validation with content too long"""
    provider = SecondarySmsApiProvider()
    long_content = "A" * 161
    with pytest.raises(errors.InvalidContentLength):
        provider.set_content(long_content)


def test_secondary_provider_validate_content_max_length():
    """Test content validation with maximum allowed length"""
    provider = SecondarySmsApiProvider()
    max_content = "A" * 160
    provider.set_content(max_content)
    assert len(provider.content) == 160


def test_secondary_provider_validate_before_sending_missing_content():
    """Test validation before sending when content is missing"""
    provider = SecondarySmsApiProvider()
    provider.set_recipient(600123456)
    with pytest.raises(errors.ContentNotSet):
        provider.send()


def test_secondary_provider_validate_before_sending_missing_recipient():
    """Test validation before sending when recipient is missing"""
    provider = SecondarySmsApiProvider()
    provider.set_content("Hello")
    with pytest.raises(errors.RecipientNotSet):
        provider.send()


def test_secondary_provider_prepare_payload():
    """Test payload preparation"""
    provider = SecondarySmsApiProvider()
    provider.set_recipient(600123456).set_content("Hello")
    payload = provider._prepare_payload()
    assert payload["body"] == "Hello"
    assert payload["recipient"] == "0048600123456"
    assert payload["sender_name"] == "Alice"
    assert payload["auth_key"] == "bob"


def test_secondary_provider_process_response_ok():
    """Test response processing for OK status"""
    provider = SecondarySmsApiProvider()
    response = {"status": "OK", "id": "test-id"}
    success, resp = provider._process_response(response)
    assert success is True
    assert resp == response


def test_secondary_provider_process_response_not_ok():
    """Test response processing for non-OK status"""
    provider = SecondarySmsApiProvider()
    response = {"status": "403", "error": "Invalid key"}
    success, resp = provider._process_response(response)
    assert success is False
    assert resp == response


def test_secondary_provider_chainable():
    """Test that all methods are chainable"""
    provider = SecondarySmsApiProvider()
    result = provider.set_recipient(600123456).set_content("Hello")
    assert result is provider


def test_secondary_provider_different_country():
    """Test provider with different country code"""
    provider = SecondarySmsApiProvider()
    success, response = provider.set_recipient(600123456, "DE").set_content("Hello").send()
    assert success is True


def test_secondary_provider_api_key():
    """Test that API_KEY is set correctly"""
    provider = SecondarySmsApiProvider()
    assert provider.API_KEY == "bob"


def test_secondary_provider_content_limit_difference():
    """Test that secondary provider allows longer content than primary"""
    provider = SecondarySmsApiProvider()
    # 160 characters should work for secondary
    long_content = "A" * 160
    provider.set_content(long_content)
    assert len(provider.content) == 160
    
    # But 161 should fail
    with pytest.raises(errors.InvalidContentLength):
        provider.set_content("A" * 161)


def test_secondary_provider_payload_structure_difference():
    """Test that secondary provider uses different payload structure than primary"""
    provider = SecondarySmsApiProvider()
    provider.set_recipient(600123456).set_content("Hello")
    payload = provider._prepare_payload()
    # Secondary uses "body" instead of "content"
    assert "body" in payload
    assert "content" not in payload
    # Secondary uses "auth_key" instead of "api_key"
    assert "auth_key" in payload
    assert "api_key" not in payload
    # Secondary uses "sender_name" instead of "sender"
    assert "sender_name" in payload
    assert "sender" not in payload

