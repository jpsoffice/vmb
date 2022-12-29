from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from .tasks import send_batch_matches_emails

from actstream import registry

class MatrimonyConfig(AppConfig):
    name = "vmb.matrimony"
    verbose_name = _("Matrimony")

    def ready(self):
        from vmb.users import User
        registry.register(User, self.get_model('MatrimonyProfile'))

