import datetime
from dateutil.relativedelta import relativedelta
from admin_numeric_filter.admin import (
    NumericFilterModelAdmin,
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter,
    RangeNumericForm,
)
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    ChoiceDropdownFilter,
    RelatedDropdownFilter,
)
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.fields import DateField
from django.utils import timezone
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
from djmoney.money import Money
from .forms import TextRangeForm
from moneyed.classes import CurrencyDoesNotExist
from decimal import InvalidOperation
from django.core.exceptions import ValidationError


class RoundsFilter(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = "rounds of chanting"

    # Parameter for the filter that will be used in the URL query.
    parameter_name = "rounds_chanting"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ("16", (">=16")),
            ("8-16", ("8-16")),
            ("1-8", ("1-8")),
            ("0", ("Does not chant")),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        if self.value() == "16":
            return queryset.filter(rounds_chanting__gte=int(16))
        if self.value() == "8-16":
            return queryset.filter(
                rounds_chanting__lt=int(16), rounds_chanting__gte=int(8)
            )
        if self.value() == "1-8":
            return queryset.filter(
                rounds_chanting__lt=int(8), rounds_chanting__gte=int(1)
            )
        if self.value() == "0":

            return queryset.filter(rounds_chanting__lte=int(0))


class AnnualIncomeRangeFilter(admin.SimpleListFilter):
    title = "Annual Income"
    request = None
    parameter_name = "currency"
    field_name = "annual_income"
    template = "admin/input_filter.html"

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

        self.request = request
        if self.parameter_name + "_from" in params:
            value = params.pop(self.parameter_name + "_from")
            value_list = value.split()
            if len(value_list) == 2:
                from_income = value_list[0]
                from_currency = value_list[1]
                try:
                    self.used_parameters[self.field_name + "_from"] = Money(
                        from_income, from_currency
                    )
                except:
                    pass
                self.used_parameters[self.parameter_name + "_from"] = value

        if self.parameter_name + "_to" in params:
            value = params.pop(self.parameter_name + "_to")
            value_list = value.split()
            if len(value_list) == 2:
                to_income = value_list[0]
                to_currency = value_list[1]
                try:
                    self.used_parameters[self.field_name + "_to"] = Money(
                        to_income, to_currency
                    )
                except:
                    pass
                self.used_parameters[self.parameter_name + "_to"] = value

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.field_name + "_from", None)
        if value_from is not None:
            filters.update({self.field_name + "__gte": value_from})

        value_to = self.used_parameters.get(self.field_name + "_to", None)
        if value_to is not None and value_to != "":
            filters.update(
                {self.field_name + "__lte": value_to,}
            )

        return queryset.filter(**filters)

    def lookups(self, request, model_admin):
        return []

    def has_output(self):
        return True

    def expected_parameters(self):
        return [
            "{}_from".format(self.parameter_name),
            "{}_to".format(self.parameter_name),
        ]

    def choices(self, changelist):
        return (
            {
                "request": self.request,
                "parameter_name": self.parameter_name,
                "form": TextRangeForm(
                    name=self.parameter_name,
                    data={
                        self.parameter_name
                        + "_from": self.used_parameters.get(
                            self.parameter_name + "_from", None
                        ),
                        self.parameter_name
                        + "_to": self.used_parameters.get(
                            self.parameter_name + "_to", None
                        ),
                    },
                ),
            },
        )


class AgeRangeFilter(admin.SimpleListFilter):
    title = "age"
    request = None
    parameter_name = "age"
    field_name = "dob"
    template = "admin/filter_numeric_range.html"

    def __init__(self, request, params, model, model_admin):
        super().__init__(request, params, model, model_admin)

        self.request = request

        if self.parameter_name + "_from" in params:
            value = params.pop(self.parameter_name + "_from")
            to_date = (timezone.localdate() - relativedelta(years=int(value))).strftime(
                "%Y-%m-%d"
            )
            self.used_parameters[self.parameter_name + "_from"] = value
            self.used_parameters[self.field_name + "_to"] = to_date

        if self.parameter_name + "_to" in params:
            value = params.pop(self.parameter_name + "_to")
            from_date = (
                timezone.localdate() - relativedelta(years=int(value))
            ).strftime("%Y-%m-%d")
            self.used_parameters[self.parameter_name + "_to"] = value
            self.used_parameters[self.field_name + "_from"] = from_date

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.field_name + "_from", None)
        if value_from is not None and value_from != "":
            filters.update(
                {self.field_name + "__gte": value_from,}
            )

        value_to = self.used_parameters.get(self.field_name + "_to", None)
        if value_to is not None and value_to != "":
            filters.update(
                {self.field_name + "__lte": value_to,}
            )

        return queryset.filter(**filters)

    def lookups(self, request, model_admin):
        return []

    def has_output(self):
        return True

    def expected_parameters(self):
        return [
            "{}_from".format(self.parameter_name),
            "{}_to".format(self.parameter_name),
        ]

    def choices(self, changelist):
        return (
            {
                "request": self.request,
                "parameter_name": self.parameter_name,
                "form": RangeNumericForm(
                    name=self.parameter_name,
                    data={
                        self.parameter_name
                        + "_from": self.used_parameters.get(
                            self.parameter_name + "_from", None
                        ),
                        self.parameter_name
                        + "_to": self.used_parameters.get(
                            self.parameter_name + "_to", None
                        ),
                    },
                ),
            },
        )


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
        AgeRangeFilter,
        AnnualIncomeRangeFilter,
        RoundsFilter,
        ("height", RangeNumericFilter),
        "spiritual_status",
        "marital_status",
        ("current_country", RelatedDropdownFilter),
        ("languages_known", RelatedDropdownFilter),
        ("occupation", RelatedDropdownFilter),
        ("qualification", RelatedDropdownFilter),
        ("guru", RelatedDropdownFilter),
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
