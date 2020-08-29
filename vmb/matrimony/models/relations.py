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
        return f"{self.name} ({self.code})"


class Education(BaseModel):
    """Model representing Education e.g. Bachelor, Masters, Doctorate etc"""

    name = models.CharField(max_length=255, unique=True, verbose_name=_("Degree"))
    category = models.ForeignKey(
        "EducationCategory", on_delete=models.SET_NULL, null=True
    )
    category_text = models.CharField(
        default="", max_length=75, blank=True, editable=False
    )

    def __str__(self):
        category_suffix = f" ({self.category_text})" if self.category_text else ""
        return f"{self.name}{category_suffix}"

    class Meta:
        ordering = ["name"]
        db_table = "education"
        verbose_name_plural = "Education"

    def save(self, *args, **kwargs):
        self.category_text = self.category.name or ""
        super().save(*args, **kwargs)


class EducationCategory(BaseModel):
    """Model representing Education Category e.g. Engineering, Finance etc"""

    name = models.CharField(max_length=75, unique=True)

    class Meta:
        db_table = "education_category"
        verbose_name_plural = "Education Categories"

    def __str__(self):
        return f"{self.name}"


class Occupation(BaseModel):
    """Model representing Occupation e.g. Doctor, Engineer, Entrepreneur etc"""

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        "OccupationCategory", on_delete=models.SET_NULL, null=True
    )
    category_text = models.CharField(
        default="", max_length=75, blank=True, editable=False
    )

    class Meta:
        ordering = ["name"]
        db_table = "occupations"
        unique_together = ["name", "category"]

    def __str__(self):
        category_suffix = f" ({self.category_text})" if self.category_text else ""
        return f"{self.name}{category_suffix}"

    def save(self, *args, **kwargs):
        self.category_text = self.category.name or ""
        super().save(*args, **kwargs)


class OccupationCategory(BaseModel):
    """Model representing Occupation Category e.g Administration, BPO, Civil Services etc"""

    name = models.CharField(max_length=75, unique=True)

    class Meta:
        db_table = "occupation_category"
        verbose_name_plural = "Occupation Categories"

    def __str__(self):
        return f"{self.name}"


class Religion(BaseModel):
    """Model representing Religion e.g. Hindu, Christian, Jain etc"""

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

    name = models.CharField(max_length=50)
    caste = models.ForeignKey("Caste", on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ["name"]
        db_table = "subcaste"

    def __str__(self):
        return f"{self.name}"


class Gotra(BaseModel):
    """Model representing Gotra"""

    name = models.CharField(max_length=50, null=True)

    class Meta:
        ordering = ["name"]
        db_table = "gotra"

    def __str__(self):
        return f"{self.name}"
