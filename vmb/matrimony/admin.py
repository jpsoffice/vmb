import datetime
from dateutil.relativedelta import relativedelta
from admin_numeric_filter.admin import (
    NumericFilterModelAdmin,
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter,
    RangeNumericForm,
)
from rangefilter.filter import DateTimeRangeFilter
from tabbed_admin import TabbedModelAdmin
from django import forms
from django_admin_listfilter_dropdown.filters import (
    DropdownFilter,
    ChoiceDropdownFilter,
    RelatedDropdownFilter,
)
from more_admin_filters import (
    MultiSelectRelatedDropdownFilter,
    MultiSelectFilter,
    
    )
from django_admin_multi_select_filter.filters import (MultiSelectFieldListFilter)
from djangoql.admin import DjangoQLSearchMixin
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.fields import DateField
from django.db.models import Q
from django.utils import timezone

# For enabling CKEditor for Flatpages
from django.db import models
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from django_admin_inline_paginator.admin import TabularInlinePaginated

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
    Photo,
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


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {models.TextField: {"widget": CKEditorWidget}}


# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)


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
                    {
                        self.field_name + "__lte": value_to,
                    }
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
            to_date = ""
            if value != "":
                to_date = (
                    timezone.localdate() - relativedelta(years=int(value))
                ).strftime("%Y-%m-%d")
            self.used_parameters[self.parameter_name + "_from"] = value
            self.used_parameters[self.field_name + "_to"] = to_date

        if self.parameter_name + "_to" in params:
            value = params.pop(self.parameter_name + "_to")
            from_date = ""
            if value != "":
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
                {
                    self.field_name + "__gte": value_from,
                }
            )

        value_to = self.used_parameters.get(self.field_name + "_to", None)
        if value_to is not None and value_to != "":
            filters.update(
                {
                    self.field_name + "__lte": value_to,
                }
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


class MatrimonyProfileForm(forms.ModelForm):
    class Meta:
        model = MatrimonyProfile
        fields = "__all__"

        required = [
            "birth_place",
            "current_place",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.required:
            self.fields[field].required = True


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 1
    can_delete = True

    raw_id_fields = ["photo"]

    readonly_fields = ["thumbnail"]


class BaseMatrimonyProfileAdmin(
    DjangoQLSearchMixin, NumericFilterModelAdmin, TabbedModelAdmin
):
    
    form = MatrimonyProfileForm
    change_form_template = "admin/matrimony/matrimonyprofile/change_form.html"
    tab_profile = [
        (
            None,
            {
                "fields": [
                    ("profile_id", "name", "spiritual_name"),
                    ("registration_date", "status","gender"),
                ]
            },
        ),
        (
            "CONTACT INFORMATION",
            {
                "fields": [
                    ("profile_created_by", "contact_person_name"),
                    ("phone", "email"),
                ]
            },
        ),
        (
            "BASIC INFORMATION",
            {
                "fields": [
                    ("dob","is_actual_dob", "ethnic_origin", "mother_tongue"),
                    ("languages_can_speak", "languages_can_read_write"),
                    ("rounds_chanting"),
                    ("spiritual_status", "spiritual_master"),
                    "marital_status",
                    ("height", "weight"),
                    ("body_type", "complexion"),
                    ("current_place"),
                    ("current_city", "current_state"),
                    ("current_country", "nationality"),
                    ("recreational_activities", "devotional_services"),
                    ("want_children"),
                    ("medical_history"),
                ]
            },
        ),
    ]
    tab_photo = [
        PhotoInline,
        (
            None,
            {
                "fields": [
                    "photos_visible_to_all_matches",
                ]
            },
        ),
    ]
    tab_birth_details = [
        (
            None,
            {
                "fields": [
                    ("dob", "tob", "gotra"),
                    "birth_place",
                    ("birth_state", "birth_city"),
                    ("birth_country",),
                ]
            },
        )
    ]
    tab_current_location = [
        (
            None,
            {
                "fields": [
                    "current_place",
                    ("current_state", "current_city"),
                    "current_country",
                    "nationality",
                ]
            },
        )
    ]
    tab_personal_details = [
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
        ("MEDICAL DETAILS", {"fields": ["want_children", "medical_history"]}),
    ]
    tab_professional_details = [
        (
            None,
            {
                "fields": [
                    ("occupations",),
                    ("employed_in", "organization"),
                    ("annual_income", "annual_income_in_base_currency"),
                    "occupation_details",
                    "education",
                    "institution",
                    "education_details",
                ]
            },
        )
    ]
    tab_religion_and_family = [
        (
            "RELIGIOUS INFORMATION",
            {
                "fields": [
                    ("religion"),
                    ("caste", "caste_other"),
                    ("subcaste", "subcaste_other"),
                    ("dob", "tob"),
                    ("birth_place"),
                    ("birth_city", "birth_state"),
                    ("birth_country"),
                    ("religious_background"),
                ]
            },
        ),
        (
            "FAMILY DETAILS",
            {
                "fields": [
                    ("are_parents_devotees", "family_values"),
                    ("family_type", "family_status"),
                    ("father_name","father_phone", "father_status"),
                    ("mother_name","mother_phone", "mother_status"),
                    ("brothers", "brothers_married"),
                    ("sisters", "sisters_married"),
                    ("family_location", "family_origin"),
                    ("family_details"),
                ]
            },
        ),
    ]
    list_display = (
        "profile_id",
        "id",
        "registration_date",
        "name",
        "primary_image",
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
        ("status",MultiSelectFieldListFilter),
        AgeRangeFilter,
        ("annual_income_in_base_currency", RangeNumericFilter),
        ("registration_date", DateTimeRangeFilter),
        RoundsFilter,
        ("height", RangeNumericFilter),
        ("spiritual_status",MultiSelectFieldListFilter),
        ("marital_status",MultiSelectFieldListFilter),
        ("religion", MultiSelectRelatedDropdownFilter),
        ("mother_tongue", MultiSelectRelatedDropdownFilter),
        ("caste", MultiSelectRelatedDropdownFilter),
        ("subcaste", MultiSelectRelatedDropdownFilter),
        ("current_country", MultiSelectRelatedDropdownFilter),
        ("languages_can_speak", MultiSelectRelatedDropdownFilter),
        ("occupations", MultiSelectRelatedDropdownFilter),
        ("education", MultiSelectRelatedDropdownFilter),
        ("spiritual_master", MultiSelectRelatedDropdownFilter),
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
        "primary_image",
        "annual_income_in_base_currency",
    ]

    def all_education(self, obj):
        return obj.education_text

    def all_occupations(self, obj):
        return obj.occupations_text

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        obj.refresh_from_db()
        obj.create_user()

    def delete_model(self, request, obj):
        user = obj.user
        super().delete_model(request, obj)
        if user:
            user.delete()

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


class MatchInline(TabularInlinePaginated):
    per_page = 3
    model = Match
    extra = 1
    can_delete = True

    raw_id_fields = ["male", "female"]

    verbose_name = "Match"
    verbose_name_plural = "Matches"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(
            Q(male__status=99) |Q(male__status=90) | Q(female__status=99)| Q(female__status=90)
        )  # Exclude matches with status 99 and 90 on either side

    
    


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
    tab_mentor = (MentorInline,)
    tab_expectation = (ExpectationInline,)
    tab_match = (
        CommentInline,
        MatchInline,
        MatrimonyProfileStatsInline,
    )
    tabs = [
        ("Matches & Comments", tab_match),
        ("Profile", BaseMatrimonyProfileAdmin.tab_profile),
        ("Profession", BaseMatrimonyProfileAdmin.tab_professional_details),
        ("Religion & Family", BaseMatrimonyProfileAdmin.tab_religion_and_family),
        ("Mentor", tab_mentor),
        ("Photo", BaseMatrimonyProfileAdmin.tab_photo),
        ("Expectation", tab_expectation),
        
    ]
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
    tab_mentor = (MentorInline,)
    tab_expectation = (ExpectationInline,)
    tab_match = (
        MatchInline,
        MatrimonyProfileStatsInline,
        CommentInline,
    )
    tabs = [
         ("Matches & Comments", tab_match),
        ("Profile", BaseMatrimonyProfileAdmin.tab_profile),
        ("Profession", BaseMatrimonyProfileAdmin.tab_professional_details),
        ("Religion & Family", BaseMatrimonyProfileAdmin.tab_religion_and_family),
        ("Mentor", tab_mentor),
        ("Photo", BaseMatrimonyProfileAdmin.tab_photo),
        ("Expectation", tab_expectation),
       
    ]
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
        "id",
        "category",
        "response",
        "male",
        "male_response",
        "female",
        "female_response",
        "status",
        "assignee",
        "male_response_updated_at",
        "female_response_updated_at",
        "created_by",
    )
    raw_id_fields = ("male", "female")
    inlines = [CommentInline]

    readonly_fields = ["response"]
    search_fields = [
        "male",
        "female",
    ]
    list_filter = [
        "status",
        "category",
        "created_at",
        "updated_at",
    ]

    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)

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


admin.site.register(Photo)
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
