import datetime
from admin_numeric_filter.admin import (
    NumericFilterModelAdmin,
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter,
)
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Male, Female, Guru, Language, Qualification, Occupation, Match


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


class MatchInline(admin.TabularInline):
    model = Match
    extra = 1
    can_delete = True

    raw_id_fields = ["male", "female"]

    verbose_name = "Matche"
    verbose_name_plural = "Matches"


@admin.register(Male)
class MaleAdmin(BaseMatrimonyProfileAdmin):
    model = Male
    inlines = [MatchInline]


@admin.register(Female)
class FemalAdmin(BaseMatrimonyProfileAdmin):
    model = Female
    inlines = [MatchInline]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = (
        "status",
        "assignee",
        "male",
        "male_response",
        "female",
        "female_response",
        "male_response_updated_at",
        "female_response_updated_at",
    )
    raw_id_fields = ("male", "female")
