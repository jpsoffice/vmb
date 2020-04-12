import datetime
from admin_numeric_filter.admin import (
    NumericFilterModelAdmin,
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter,
)
from django.contrib import admin
from .models import Male, Female, Guru, Language, Qualification, Occupation, Country


class BaseMatrimonyProfileAdmin(NumericFilterModelAdmin):
    fieldsets = [
        (None, {"fields": ["name", ("marital_status", "languages_known")]}),
        (
            "SPIRITUAL QUOTIENT",
            {"fields": ["rounds_chanting", ("spiritual_status", "guru")]},
        ),
        (
            "BIRTH DETAILS",
            {
                "fields": [
                    ("dob", "tob"),
                    "birth_country",
                    ("birth_state", "birth_city"),
                ]
            },
        ),
        (
            "CURRENT LOCATION",
            {"fields": ["current_country", ("current_state", "current_city")]},
        ),
        ("PHYSICAL APPEARANCE", {"fields": [("height", "complexion")]}),
        (
            "QUALIFICATON",
            {"fields": ["qualification", ("occupation", "annual_income")]},
        ),
        ("CONTACT INFORMATION", {"fields": [("phone", "email")]}),
    ]
    list_display = (
        "name",
        "age",
        "dob",
        "current_country",
        "current_city",
        "occupation",
        "annual_income",
        "phone",
        "email",
    )
    list_filter = (
        "current_state",
        "current_city",
        ("annual_income", RangeNumericFilter),
        "gender",
    )
    search_fields = [
        "name",
        "current_country__name",
        "current_state",
        "current_city",
        "occupation__occupation",
        "annual_income",
        "phone",
        "email",
    ]


@admin.register(Male)
class MaleAdmin(BaseMatrimonyProfileAdmin):
    model = Male

    def save(self, *args, **kwargs):
        self.gender = "M"
        super().save(*args, **kwargs)


@admin.register(Female)
class FemaleAdmin(BaseMatrimonyProfileAdmin):
    model = Female

    def save(self, *args, **kwargs):
        self.gender = "F"
        super().save(*args, **kwargs)


admin.site.register(Guru)
admin.site.register(Language)
admin.site.register(Qualification)
admin.site.register(Country)
admin.site.register(Occupation)



