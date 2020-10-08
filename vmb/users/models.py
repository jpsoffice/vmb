from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import CharField, BooleanField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), max_length=255, blank=True)
    phone = CharField(
        _("Phone"),
        max_length=17,
        validators=[
            RegexValidator(
                regex=r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
            )
        ],
        blank=True,
    )
    is_matrimony_candidate = BooleanField(
        _("Is matrimony candidate?"), default=False, blank=True
    )
    is_matrimony_registration_complete = BooleanField(
        _("Is matrimony registration complete?"), default=False, blank=True
    )

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
