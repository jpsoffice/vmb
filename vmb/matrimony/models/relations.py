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
        verbose_name_plural = "Countries"

    def __str__(self):
        return "{} ({})".format(self.name, self.code)


class Nationality(Country):
    class Meta:
        proxy = True

    def __str__(self):
        return self.nationality


class Language(BaseModel):
    """Model representing a Language e.g. Hindi, English, Gujrati etc"""

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


class Education(BaseModel):
    """Model representing Education e.g. Bachelor, Masters, Doctorate etc"""

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Degree"))
    category = models.ForeignKey(
        "EducationCategory", on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ["name"]
        db_table = "education"


class EducationCategory(BaseModel):
    """Model representing Education Category e.g. Engineering, Finance etc"""

    name = models.CharField(max_length=75, unique=True)

    class Meta:
        db_table = "education_category"

    def __str__(self):
        return f"{self.name}"


class Occupation(BaseModel):
    """Model representing Occupation e.g. Doctor, Engineer, Entrepreneur etc"""

    name = models.CharField(max_length=255, unique=True)
    category = models.ForeignKey(
        "OccupationCategory", on_delete=models.SET_NULL, null=True
    )

    class Meta:
        ordering = ["name"]
        db_table = "occupations"

    def __str__(self):
        return f"{self.name}"


class OccupationCategory(BaseModel):
    """Model representing Occupation Category e.g Administration, BPO, Civil Services etc"""

    name = models.CharField(max_length=75, unique=True)

    class Meta:
        db_table = "occupation_category"

    def __str__(self):
        return f"{self.name}"


class Religion(BaseModel):
    """Model representing Religion e.g. Hinduism, Christianity etc"""

    name = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
        db_table = "religion"

    def __str__(self):
        return f"{self.name}"


class Caste(BaseModel):
    """Model representing Caste e.g. Marwari, Gujarati etc"""

    name = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
        db_table = "caste"

    def __str__(self):
        return f"{self.name}"


class Subcaste(BaseModel):
    """Model representing Subcaste e.g. Brahmin, Kayastha etc"""

    name = models.CharField(max_length=20)
    caste = models.ForeignKey("Caste", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["name"]
        db_table = "subcaste"

    def __str__(self):
        return f"{self.name}"
