import datetime
from admin_numeric_filter.admin import (
    NumericFilterModelAdmin,
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter,
)
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    Male,
    Female,
    Guru,
    Language,
    Qualification,
    Occupation,
    Match,
    Country,
)


class RoundsFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = ('rounds of chanting')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'rounds_chanting'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('16', ('>=16')),
            ('8-16', ('>=8 and <16')),
            ('1-8', ('>=1 and <8')),
            ('0', ('0')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == '16':
            return queryset.filter(rounds_chanting__gte=int(16))
        if self.value() == '8-16':
            return queryset.filter(rounds_chanting__lt=int(16),
                                    rounds_chanting__gte=int(8))
        if self.value() == '1-8':
            return queryset.filter(rounds_chanting__lt=int(8),
                                    rounds_chanting__gte=int(1))    
        if self.value() == '0':
            return queryset.filter(rounds_chanting__et=int(0))                                        


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
        "current_country",
        ("annual_income", RangeNumericFilter),
        "languages_known",
        "marital_status",
        RoundsFilter,
        "occupation",
        "qualification",
        "guru",
        ("height", RangeNumericFilter),
        "spiritual_status",
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


admin.site.register(Guru)
admin.site.register(Language)
admin.site.register(Qualification)
admin.site.register(Country)
admin.site.register(Occupation)
