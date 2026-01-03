"""New SMS module"""
from app.new.providers import PrimarySmsApiProvider, SecondarySmsApiProvider


def sms_factory(api):
    """Implement a factory that creates appropriate objects based on the `api` argument. When `api` is unknown, throw NotImplementedError exception."""
    if api == 'primary':
        return PrimarySmsApiProvider()
    elif api == 'secondary':
        return SecondarySmsApiProvider()
    else:
        raise NotImplementedError(f"Unknown API: {api}")

