class BaseError(Exception):
    """Base exception class"""
    pass


class InvalidCountryException(BaseError):
    """Invalid country exception"""
    pass


class InvalidPhoneNumber(BaseError):
    """Invalid phone number"""
    pass


class InvalidContentLength(BaseError):
    """Invalid content length exception"""
    pass


class ContentNotSet(BaseError):
    """Content not set exception"""
    pass


class RecipientNotSet(BaseError):
    """Recipient not set exception"""
    pass

