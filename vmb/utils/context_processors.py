from django.conf import settings


def extra_context(_request):
    return {
        "METRICS_BACKEND": settings.METRICS_BACKEND,
        "POSTHOG_API_KEY": settings.POSTHOG_API_KEY,
        "POSTHOG_HOST": settings.POSTHOG_HOST,
    }
