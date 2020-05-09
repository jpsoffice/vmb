from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .tasks import send_email, send_batch_matches_emails


class MatrimonyConfig(AppConfig):
    name = "vmb.matrimony"
    verbose_name = _("Matrimony")
