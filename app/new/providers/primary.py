from app import settings, errors
from app.fake import fake_primary_external_api
from app.new.providers.base import BaseSmsProvider


class PrimarySmsApiProvider(BaseSmsProvider):
    """Primary SMS API Provider"""
    API_KEY = settings.PRIMARY_API_KEY

    def _validate_set_recipient(self, phone_number, country_code="PL"):
        """Validate recipient using the same logic as defined in `old.py` file. Throw appropriate exception or return a boolean"""
        if country_code and country_code not in self.COUNTRY_CODES.keys():
            raise errors.InvalidCountryException("Invalid country code")
        if not str(phone_number).isdigit():
            raise errors.InvalidPhoneNumber("Invalid phone number")

    def _validate_set_content(self, content):
        """Validate content. Throw appropriate exception or return a boolean"""
        if len(content) > 70:
            raise errors.InvalidContentLength("Invalid content length")

    def _validate_before_sending(self):
        """Check if content and recipient are set. Throw appropriate exception from `app.errors` module"""
        if self.content is None:
            raise errors.ContentNotSet("Content not set")
        if self.recipient is None:
            raise errors.RecipientNotSet("Recipient not set")

    def _process_response(self, resp):
        """Check response content. Return (boolean, resp)"""
        if resp.get("status") == "SENT":
            return True, resp
        return False, resp

    def _prepare_payload(self):
        """Construct and return payload - check `old.py` for the implementation details"""
        return {
            "content": self.content,
            "phone": self.recipient,
            "sender": self.SENDER_NAME,
            "api_key": self.API_KEY,
        }

    def send(self):
        """Send the message"""
        self._validate_before_sending()
        payload = self._prepare_payload()
        response = fake_primary_external_api(payload)
        return self._process_response(response)

