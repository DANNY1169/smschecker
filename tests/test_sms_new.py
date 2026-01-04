"""Tests for the new SMS API implementation"""
import pytest

from app import errors
from app.new import sms_factory


def test_new_sms_primary_success():
    """Test successful primary SMS using new implementation"""
    success, response = sms_factory('primary').set_recipient(600123456).set_content('Hello').send()
    assert success is True
    assert response["status"] == "SENT"
    assert response["recipient"] == "0048600123456"


def test_new_sms_primary_chainable():
    """Test that new SMS methods are chainable"""
    provider = sms_factory('primary')
    result = provider.set_recipient(600123456).set_content('Hello')
    assert result is provider


def test_new_sms_primary_invalid_country_code():
    """Test new primary SMS with invalid country code"""
    with pytest.raises(errors.InvalidCountryException):
        sms_factory('primary').set_recipient(600123456, 'XX').set_content('Hello')


def test_new_sms_primary_invalid_phone_number():
    """Test new primary SMS with invalid phone number"""
    with pytest.raises(errors.InvalidPhoneNumber):
        sms_factory('primary').set_recipient('600-123-456').set_content('Hello')


def test_new_sms_primary_invalid_content_length():
    """Test new primary SMS with content too long"""
    long_content = "A" * 71
    with pytest.raises(errors.InvalidContentLength):
        sms_factory('primary').set_recipient(600123456).set_content(long_content)


def test_new_sms_primary_content_not_set():
    """Test new primary SMS without setting content"""
    with pytest.raises(errors.ContentNotSet):
        sms_factory('primary').set_recipient(600123456).send()


def test_new_sms_primary_recipient_not_set():
    """Test new primary SMS without setting recipient"""
    with pytest.raises(errors.RecipientNotSet):
        sms_factory('primary').set_content('Hello').send()


def test_new_sms_primary_default_country_code():
    """Test new primary SMS with default country code"""
    success, response = sms_factory('primary').set_recipient(600123456).set_content('Hello').send()
    assert success is True
    assert response["recipient"] == "0048600123456"


def test_new_sms_primary_different_country():
    """Test new primary SMS with different country code"""
    success, response = sms_factory('primary').set_recipient(600123456, 'DE').set_content('Hello').send()
    assert success is True
    assert response["recipient"] == "0049600123456"


def test_new_sms_secondary_success():
    """Test successful secondary SMS using new implementation"""
    success, response = sms_factory('secondary').set_recipient(600123456).set_content('Hello').send()
    assert success is True
    assert response["status"] == "OK"
    assert "id" in response


def test_new_sms_secondary_chainable():
    """Test that new secondary SMS methods are chainable"""
    provider = sms_factory('secondary')
    result = provider.set_recipient(600123456).set_content('Hello')
    assert result is provider


def test_new_sms_secondary_invalid_country_code():
    """Test new secondary SMS with invalid country code"""
    with pytest.raises(errors.InvalidCountryException):
        sms_factory('secondary').set_recipient(600123456, 'XX').set_content('Hello')


def test_new_sms_secondary_invalid_phone_number():
    """Test new secondary SMS with invalid phone number"""
    with pytest.raises(errors.InvalidPhoneNumber):
        sms_factory('secondary').set_recipient('600-123-456').set_content('Hello')


def test_new_sms_secondary_invalid_content_length():
    """Test new secondary SMS with content too long"""
    long_content = "A" * 161
    with pytest.raises(errors.InvalidContentLength):
        sms_factory('secondary').set_recipient(600123456).set_content(long_content)


def test_new_sms_secondary_content_not_set():
    """Test new secondary SMS without setting content"""
    with pytest.raises(errors.ContentNotSet):
        sms_factory('secondary').set_recipient(600123456).send()


def test_new_sms_secondary_recipient_not_set():
    """Test new secondary SMS without setting recipient"""
    with pytest.raises(errors.RecipientNotSet):
        sms_factory('secondary').set_content('Hello').send()


def test_new_sms_secondary_default_country_code():
    """Test new secondary SMS with default country code"""
    success, response = sms_factory('secondary').set_recipient(600123456).set_content('Hello').send()
    assert success is True


def test_new_sms_secondary_different_country():
    """Test new secondary SMS with different country code"""
    success, response = sms_factory('secondary').set_recipient(600123456, 'DE').set_content('Hello').send()
    assert success is True


def test_new_sms_usage_example():
    """Test the usage example from README"""
    success, response = sms_factory('primary').set_recipient(600123456).set_content('Foo Bar').send()
    assert success is True
    assert response["status"] == "SENT"

