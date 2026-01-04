"""Tests for the base SMS provider class"""
import pytest

from app.new.providers.base import BaseSmsProvider
from app.new.providers import PrimarySmsApiProvider, SecondarySmsApiProvider


def test_base_provider_is_abstract():
    """Test that BaseSmsProvider cannot be instantiated directly"""
    with pytest.raises(TypeError):
        BaseSmsProvider()


def test_base_provider_set_content():
    """Test that set_content sets the content attribute"""
    provider = PrimarySmsApiProvider()
    result = provider.set_content("Hello World")
    assert provider.content == "Hello World"
    assert result is provider


def test_base_provider_set_recipient():
    """Test that set_recipient sets the recipient attribute"""
    provider = PrimarySmsApiProvider()
    result = provider.set_recipient(600123456)
    assert provider.recipient == "0048600123456"
    assert result is provider


def test_base_provider_set_recipient_with_country_code():
    """Test that set_recipient works with country code"""
    provider = PrimarySmsApiProvider()
    result = provider.set_recipient(600123456, "DE")
    assert provider.recipient == "0049600123456"
    assert result is provider


def test_base_provider_chainable_methods():
    """Test that set_content and set_recipient are chainable"""
    provider = PrimarySmsApiProvider()
    result = provider.set_content("Hello").set_recipient(600123456)
    assert result is provider
    assert provider.content == "Hello"
    assert provider.recipient == "0048600123456"


def test_base_provider_sender_name():
    """Test that SENDER_NAME is set correctly"""
    provider = PrimarySmsApiProvider()
    assert provider.SENDER_NAME == "Alice"


def test_base_provider_country_codes():
    """Test that COUNTRY_CODES are accessible"""
    provider = PrimarySmsApiProvider()
    assert "PL" in provider.COUNTRY_CODES
    assert "DE" in provider.COUNTRY_CODES
    assert provider.COUNTRY_CODES["PL"] == "0048"
    assert provider.COUNTRY_CODES["DE"] == "0049"


def test_base_provider_initial_state():
    """Test that recipient and content are None initially"""
    provider = PrimarySmsApiProvider()
    assert provider.recipient is None
    assert provider.content is None


def test_base_provider_abstract_methods():
    """Test that subclasses must implement abstract methods"""
    # PrimarySmsApiProvider should implement all abstract methods
    provider = PrimarySmsApiProvider()
    assert hasattr(provider, 'send')
    assert hasattr(provider, '_process_response')
    assert hasattr(provider, '_prepare_payload')
    
    # SecondarySmsApiProvider should also implement all abstract methods
    provider2 = SecondarySmsApiProvider()
    assert hasattr(provider2, 'send')
    assert hasattr(provider2, '_process_response')
    assert hasattr(provider2, '_prepare_payload')

