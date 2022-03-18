from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from . import get_backend


class MetricsConfig(AppConfig):
    name = "vmb.metrics"
    verbose_name = _("Metrics")

    def ready(self):
        backend = get_backend()
        backend.init()
