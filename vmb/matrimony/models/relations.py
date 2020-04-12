from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base import BaseModel


class Guru(BaseModel):
    """Model for representing an Initiating Guru"""

    name = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "gurus"
        ordering = ["name"]


class Country(BaseModel):
    name = models.CharField(
        max_length=255, unique=True, db_index=True, help_text=_("Name")
    )
    code = models.CharField(
        max_length=3, unique=True, db_index=True, help_text=_("Code")
    )
    nationality = models.CharField(
        max_length=255, unique=True, db_index=True, help_text=_("Nationality")
    )

    class Meta:
        db_table = "countries"
        ordering = ["name"]

    def __str__(self):
        return "{} ({})".format(self.name, self.code)


class Nationality(Country):
    class Meta:
        proxy = True

    def __str__(self):
        return self.nationality


class Language(BaseModel):
    """Model representing a Language(e.g. Hindi, English, Gujrati etc.)"""

    name = models.CharField(
        max_length=255, unique=True, db_index=True, verbose_name=_("Language")
    )
    code = models.CharField(
        max_length=3, unique=True, db_index=True, verbose_name=_("Language Code")
    )

    class Meta:
        db_table = "languages"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.code}"


class Qualification(BaseModel):
    """Model representing Degree(e.g. Bachelor, Masters, Doctorate etc.)"""

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Degree"))

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        db_table = "qualifications"


class Occupation(BaseModel):
    """Model representing Occupation(e.g. Doctor, Engineer, Entrepreneur etc.)"""

    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name"]
        db_table = "occupations"

    def __str__(self):
        return f"{self.name}"
