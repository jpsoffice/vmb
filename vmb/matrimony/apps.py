from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .tasks import send_batch_matches_emails


class MatrimonyConfig(AppConfig):
    name = "vmb.matrimony"
    verbose_name = _("Matrimony")

    def ready(self):
        from actstream import registry
        from vmb.users.models import User
        registry.register(User,self.get_model('MatrimonyProfile'))

