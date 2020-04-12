import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from vmb.users.models import User
from djmoney.models.fields import MoneyField

from .base import BaseModel
from .relations import Occupation, Qualification, Guru, Language, Country

GENDER_CHOICES = (("M", "Male"), ("F", "Female"), ("O", "Others"))

SPIRITUAL_STATUS_CHOICES = (
    ("A", "Aspiring"),
    ("S", "Shelter"),
    ("D1", "Harinam"),
    ("D2", "Brahmin"),
)

COMPLEXION_CHOICES = (
    ("FAI", _("Fair")),
    ("VFA", _("Very fair")),
    ("WHT", _("Wheatish")),
    ("WHB", _("Wheatish brown")),
    ("DAR", _("Dark")),
)
# Create your models here.
MARITAL_STATUS = (
    ("UMR", "Unmarried"),
    ("ENG", "Engaged"),
    ("SEP", "Separated"),
    ("DIV", "Divorced"),
    ("WID", "Widowed"),
)


class MatrimonyProfile(BaseModel):
    """Model representing matrimonial profile of a candidate"""

    name = models.CharField(max_length=200, verbose_name=_("Name"),)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,)

    # Spiritual details
    rounds_chanting = models.PositiveIntegerField(
        verbose_name=_("Rounds"),
        help_text="How many rounds are you chanting?",
        default=0,
    )
    spiritual_status = models.CharField(
        max_length=2,
        help_text="Enter spiritual status (e.g. Aspiring, Shelter etc.)",
        choices=SPIRITUAL_STATUS_CHOICES,
        verbose_name=_("Siksha Status"),
        blank=True,
    )
    guru = models.ForeignKey("Guru", on_delete=models.SET_NULL, null=True, blank=True)

    # Birth details
    dob = models.DateField(
        help_text="Enter birth date as YYYY-MM-DD",
        verbose_name=_("Birth Date"),
        null=True,
    )
    tob = models.TimeField(
        help_text="Enter time HH:MM:SS in 24hr format",
        verbose_name=_("Birth Time"),
        null=True,
    )
    birth_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text="Enter birth village/town/city",
        null=True,
    )
    birth_state = models.CharField(max_length=200, verbose_name=_("State"), null=True)
    birth_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="birthCountry",
        verbose_name=_("Country"),
    )

    # Current location details
    current_city = models.CharField(
        max_length=200,
        verbose_name=_("City"),
        help_text="Enter current village/town/city",
        null=True,
    )
    current_state = models.CharField(
        max_length=200, verbose_name=_("State"), null=True,
    )
    current_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="currentCountry",
        verbose_name=_("Country"),
    )

    # Personal details
    languages_known = models.ManyToManyField(
        "Language", help_text="Add the language you know"
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Height in cms",
        blank=True,
        null=True,
    )
    complexion = models.CharField(
        max_length=3,
        help_text="Enter your complexion",
        choices=COMPLEXION_CHOICES,
        blank=True,
        null=True,
    )
    qualification = models.ForeignKey(
        "Qualification",
        on_delete=models.SET_NULL,
        null=True,
        help_text="H.S., Graduate etc.",
    )
    occupation = models.ForeignKey(
        "Occupation",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Surgeon, Computer Application Engineer, etc.",
    )
    annual_income = MoneyField(
        max_digits=10, decimal_places=2, null=True, default_currency="INR"
    )
    marital_status = models.CharField(
        max_length=3,
        choices=MARITAL_STATUS,
        help_text="Single, Divorced etc.",
        null=True,
    )

    # Contact details
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email"))
    phone = models.CharField(max_length=17, verbose_name=_("Phone number"), null=True,)

    expectations = models.TextField(max_length=300, null=True)

    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )

    # Staff users
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_profiles",
    )

    def age(self):
        if self.dob:
            return int((datetime.datetime.now().date() - self.dob).days / 365.25)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "matrimony_profiles"


class MaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gender="M")


class Male(MatrimonyProfile):
    objects = MaleManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.gender = "M"
        super().save(*args, **kwargs)


class FemaleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(gender="F")


class Female(MatrimonyProfile):
    objects = FemaleManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        self.gender = "F"
        super().save(*args, **kwargs)
