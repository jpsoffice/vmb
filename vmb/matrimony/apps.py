from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

import posthog

from .tasks import send_batch_matches_emails


class MatrimonyConfig(AppConfig):
    name = "vmb.matrimony"
    verbose_name = _("Matrimony")

    def ready(self):
        from django.conf import settings

        posthog.api_key = settings.POSTHOG_API_KEY
        posthog.host = settings.POSTHOG_HOST
