from django.apps import AppConfig, apps
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "vmb.users"
    verbose_name = _("Users")

    def ready(self):
        try:
            import vmb.users.signals  # noqa F401
        except ImportError:
            pass
