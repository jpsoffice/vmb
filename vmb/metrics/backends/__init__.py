def get_backend():
    from django.conf import settings

    backend = importlib.import_module(settings.METRICS_BACKEND)
    return backend
