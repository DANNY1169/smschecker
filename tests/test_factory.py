"""Tests for the SMS factory function"""
import pytest

from app.new import sms_factory
from app.new.providers import PrimarySmsApiProvider, SecondarySmsApiProvider


def test_factory_returns_primary_provider():
    """Test that factory returns PrimarySmsApiProvider for 'primary'"""
    provider = sms_factory('primary')
    assert isinstance(provider, PrimarySmsApiProvider)


def test_factory_returns_secondary_provider():
    """Test that factory returns SecondarySmsApiProvider for 'secondary'"""
    provider = sms_factory('secondary')
    assert isinstance(provider, SecondarySmsApiProvider)


def test_factory_raises_not_implemented_error():
    """Test that factory raises NotImplementedError for unknown API"""
    with pytest.raises(NotImplementedError):
        sms_factory('unknown')


def test_factory_raises_not_implemented_error_for_empty_string():
    """Test that factory raises NotImplementedError for empty string"""
    with pytest.raises(NotImplementedError):
        sms_factory('')


def test_factory_raises_not_implemented_error_for_none():
    """Test that factory raises NotImplementedError for None"""
    with pytest.raises(NotImplementedError):
        sms_factory(None)

