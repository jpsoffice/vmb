from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .tasks import hello


class MatrimonyConfig(AppConfig):
    name = "vmb.matrimony"
    verbose_name = _("Matrimony")
