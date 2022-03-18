import posthog as _posthog


def init():
    """
    Initialize posthog metrics backend
    """
    from django.conf import settings

    _posthog.api_key = settings.POSTHOG_API_KEY
    _posthog.host = settings.POSTHOG_HOST


def count(uid, event, property=None, timestamp=None):
    """
    Capture posthog metrics
    """
    _posthog.capture(uid, event, property, timestamp)
