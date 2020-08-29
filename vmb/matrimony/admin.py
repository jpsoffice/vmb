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
from djangoql.admin import DjangoQLSearchMixin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.fields import DateField
from django.utils import timezone

from .models.profiles import MatrimonyProfile
from .models import (
    Male,
    Female,
    MatrimonyProfileStats,
    Guru,
    Nationality,
    Language,
    Education,
    EducationCategory,
    Occupation,
    OccupationCategory,
    Match,
    Country,
    Caste,
    Subcaste,
    Religion,
    Expectation,
    Comment,
    Mentor,
    Gotra,
)
from djmoney.money import Money
from .forms import TextRangeForm
from moneyed.classes import CurrencyDoesNotExist
from decimal import InvalidOperation
from builtins import IndexError


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
                self.used_parameters[self.field_name + "_from"] = Money(
                    from_income, from_currency
                )
                self.used_parameters[self.parameter_name + "_from"] = value

        if self.parameter_name + "_to" in params:
            value = params.pop(self.parameter_name + "_to")
            value_list = value.split()
            if len(value_list) == 2:
                to_income = value_list[0]
                to_currency = value_list[1]
                self.used_parameters[self.field_name + "_to"] = Money(
                    to_income, to_currency
                )
                self.used_parameters[self.parameter_name + "_to"] = value

    def queryset(self, request, queryset):
        filters = {}

        value_from = self.used_parameters.get(self.field_name + "_from", None)
        if value_from is not None:
            try:
                filters.update({self.field_name + "__gte": value_from})
            except (CurrencyDoesNotExist, InvalidOperation):
                pass

        value_to = self.used_parameters.get(self.field_name + "_to", None)
        if value_to is not None and value_to != "":
            try:
                filters.update(
                    {self.field_name + "__lte": value_to,}
                )
            except (CurrencyDoesNotExist, InvalidOperation):
                pass

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


class MentorInline(admin.TabularInline):
    model = Mentor
    extra = 1
    can_delete = True

    verbose_name = "Mentor"
    verbose_name_plural = "Mentors"


class MatrimonyProfileStatsInline(admin.TabularInline):
    model = MatrimonyProfileStats
    extra = 0
    can_delete = False

    readonly_fields = [
        "matches_suggested",
        "matches_accepted",
        "matches_rejected",
        "matches_accepted_by",
        "matches_rejected_by",
    ]

    verbose_name = "Stats"
    verbose_name_plural = "Stats"

    def has_add_permission(self, request, obj=None):
        return False


class BaseMatrimonyProfileAdmin(DjangoQLSearchMixin, NumericFilterModelAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": [
                    ("profile_id", "name", "spiritual_name"),
                    ("status", "ethnic_origin"),
                    ("age", "mother_tongue", "marital_status", "children_count"),
                    ("religion", "caste", "subcaste"),
                    ("languages_known", "languages_read_write"),
                ]
            },
        ),
        ("CONTACT INFORMATION", {"fields": [("phone", "email")]}),
        (
            "BIRTH DETAILS",
            {
                "fields": [
                    ("dob", "tob", "gotra"),
                    "birth_place",
                    ("birth_state", "birth_city"),
                    ("birth_country",),
                ]
            },
        ),
        (
            "SPIRITUAL QUOTIENT",
            {"fields": [("rounds_chanting", "spiritual_status", "spiritual_master")]},
        ),
        (
            "CURRENT LOCATION",
            {
                "fields": [
                    "current_place",
                    ("current_state", "current_city"),
                    "current_country",
                    "nationality",
                ]
            },
        ),
        (
            "PHYSICAL APPEARANCE",
            {
                "fields": [
                    ("height", "complexion"),
                    ("weight", "body_type"),
                    ("hair_color", "color_of_eyes"),
                ]
            },
        ),
        (
            "PERSONALITY",
            {
                "fields": [
                    "personality",
                    ("recreational_activities", "devotional_services"),
                ]
            },
        ),
        (
            "PROFESSION",
            {
                "fields": [
                    ("annual_income", "annual_income_in_base_currency"),
                    ("education", "institution"),
                    "education_details",
                    "employed_in",
                    ("occupations", "organization"),
                    "occupation_details",
                ]
            },
        ),
        (
            "FAMILY DETAILS",
            {
                "fields": [
                    (
                        "are_parents_devotees",
                        "family_values",
                        "family_type",
                        "family_status",
                    ),
                    ("father_status", "mother_status"),
                    ("brothers", "brothers_married"),
                    ("sisters", "sisters_married"),
                    ("family_location", "family_origin"),
                ]
            },
        ),
        ("MEDICAL DETAILS", {"fields": ["want_children", "medical_history"]}),
    ]
    list_display = (
        "profile_id",
        "name",
        # "primary_image",
        "status",
        "age",
        "dob",
        "annual_income",
        "current_country",
        "current_city",
        "all_occupations",
        "all_education",
        "phone",
        "email",
    )
    list_filter = (
        "status",
        AgeRangeFilter,
        # AnnualIncomeRangeFilter,
        ("annual_income_in_base_currency", RangeNumericFilter),
        RoundsFilter,
        ("height", RangeNumericFilter),
        "spiritual_status",
        "marital_status",
        ("religion", RelatedDropdownFilter),
        ("mother_tongue", RelatedDropdownFilter),
        ("caste", RelatedDropdownFilter),
        ("subcaste", RelatedDropdownFilter),
        ("current_country", RelatedDropdownFilter),
        ("languages_known", RelatedDropdownFilter),
        ("occupations", RelatedDropdownFilter),
        ("education", RelatedDropdownFilter),
        ("spiritual_master", RelatedDropdownFilter),
    )
    search_fields = [
        "name",
        "current_country__name",
        "current_state",
        "current_city",
        "annual_income_in_base_currency",
        "phone",
        "email",
        "spiritual_status",
        "marital_status",
        "ethnic_origin__nationality",
        "mother_tongue__name",
        "caste__name",
        "spiritual_master__name",
        "education__name",
        "occupations__name",
    ]

    readonly_fields = [
        "profile_id",
        "age",
        # "primary_image",
        "annual_income_in_base_currency",
        "current_city",
        "current_state",
        "current_country",
        "birth_city",
        "birth_state",
        "birth_country",
    ]

    def all_education(self, obj):
        return obj.education_text

    def all_occupations(self, obj):
        return obj.occupations_text

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

        if "Comment" in str(formset.model):
            for item in formset.new_objects + formset.changed_objects:
                # This is because formset.changed_objects is a list of tuples
                if isinstance(item, tuple):
                    obj = item[0]
                else:
                    obj = item
                obj.author = request.user
                obj.save()

    # inlines = [MentorInline]


class MatchInline(admin.TabularInline):
    model = Match
    extra = 1
    can_delete = True

    raw_id_fields = ["male", "female"]

    verbose_name = "Matche"
    verbose_name_plural = "Matches"


class PhotoInline(admin.TabularInline):
    model = MatrimonyProfile.images.through
    extra = 1
    can_delete = True

    raw_id_fields = ["photo"]


class ExpectationInline(admin.StackedInline):
    model = Expectation
    extra = 0
    can_delete = False
    readonly_fields = (
        "annual_income_from_in_base_currency",
        "annual_income_to_in_base_currency",
    )

    def get_extra(self, request, obj=None, **kwargs):
        extra = 1
        if obj and hasattr(obj, "expectations"):
            extra = 0
        return extra


class CommentInline(GenericTabularInline):
    model = Comment
    extra = 1
    can_delete = True


@admin.register(Male)
class MaleAdmin(BaseMatrimonyProfileAdmin):
    model = Male
    inlines = [
        MentorInline,
        PhotoInline,
        ExpectationInline,
        MatchInline,
        CommentInline,
        MatrimonyProfileStatsInline,
    ]


@admin.register(Female)
class FemalAdmin(BaseMatrimonyProfileAdmin):
    model = Female
    inlines = [
        MentorInline,
        PhotoInline,
        ExpectationInline,
        MatchInline,
        CommentInline,
        MatrimonyProfileStatsInline,
    ]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    model = Match
    list_display = (
        "male",
        "male_response",
        "female",
        "female_response",
        "status",
        "assignee",
        "male_response_updated_at",
        "female_response_updated_at",
    )
    raw_id_fields = ("male", "female")
    inlines = [CommentInline]

    def save_formset(self, request, form, formset, change):
        super().save_formset(request, form, formset, change)

        if "Comment" in str(formset.model):
            for item in formset.new_objects + formset.changed_objects:
                # This is because formset.changed_objects is a list of tuples
                if isinstance(item, tuple):
                    obj = item[0]
                else:
                    obj = item
                obj.author = request.user
                obj.save()


admin.site.register(Caste)
admin.site.register(Subcaste)
admin.site.register(Religion)
admin.site.register(Guru)
admin.site.register(Language)
admin.site.register(Education)
admin.site.register(Country)
admin.site.register(Occupation)
admin.site.register(EducationCategory)
admin.site.register(OccupationCategory)
admin.site.register(Nationality)
admin.site.register(Gotra)
