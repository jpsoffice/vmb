import importlib


def get_backend():
    from django.conf import settings

    backend = importlib.import_module(
        "vmb.metrics.backends." + settings.METRICS_BACKEND
    )
    return backend


def count(uid, event, property=None, timestamp=None):
    backend = get_backend()
    backend.count(uid, event, property, timestamp)
