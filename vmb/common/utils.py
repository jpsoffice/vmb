from django.conf import settings
from django.contrib.sites.models import Site


def build_absolute_url(path):
    """
    Builds absolute URL from relative path.
    """
    site = Site.objects.get_current()
    proto = settings.DEFAULT_HTTP_PROTOCOL
    return f"{proto}://{site.domain}{path}"
