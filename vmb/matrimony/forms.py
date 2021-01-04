import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from allauth.account.forms import SignupForm as AllAuthSignupForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Field, Submit

from multiselectfield import MultiSelectFormField

from vmb.matrimony.models.profiles import (
    GENDER_CHOICES,
    PROFILE_CREATED_BY_CHOICES,
    MARITAL_STATUS,
    SPIRITUAL_STATUS_CHOICES,
    MatrimonyProfile,
    Expectation,
)


class TextRangeForm(forms.Form):
    name = None

    def __init__(self, *args, **kwargs):
        self.name = kwargs.pop("name")
        super().__init__(*args, **kwargs)

        self.fields[self.name + "_from"] = forms.CharField(
            label="",
            required=False,
            widget=forms.TextInput(attrs={"placeholder": _("From")}),
        )
        self.fields[self.name + "_to"] = forms.CharField(
            label="",
            required=False,
            widget=forms.TextInput(attrs={"placeholder": _("To")}),
        )

    class Media:
        css = {"all": ("css/admin-numeric-filter.css",)}


class SignupForm(AllAuthSignupForm):
    name = forms.CharField(min_length=3, max_length=200, strip=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    marital_status = forms.ChoiceField(choices=MARITAL_STATUS)
    phone = forms.CharField(
        min_length=10,
        max_length=17,
        validators=[
            RegexValidator(
                regex=r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
            )
        ],
    )
    dob = forms.DateField(
        label=_("Date of birth"),
        widget=forms.DateInput(
            format=("%b %d, %Y"),
            attrs={
                "class": "form-control datepicker",
                "data-provide": "datepicker",
                "data-date-format": "M dd, yyyy",
                "data-date-autoclose": "true",
            },
        ),
        input_formats=("%b %d, %Y",),
    )
    rounds_chanting = forms.IntegerField(min_value=1, max_value=192)
    profile_created_by = forms.ChoiceField(choices=PROFILE_CREATED_BY_CHOICES)
    contact_person_name = forms.CharField(
        min_length=3, max_length=200, strip=True, required=False
    )

    def clean_dob(self):
        value = self.cleaned_data["dob"]
        if ((timezone.now().date() - value).days / 365.25) < 18:
            raise forms.ValidationError(_("Age is less than 18 years!"))
        return value

    def clean_phone(self):
        value = self.cleaned_data["phone"]
        if MatrimonyProfile.objects.filter(phone=value):
            raise forms.ValidationError(_("Phone number already exists."))
        return value

    def clean_contact_person_name(self):
        contact_person_name = self.cleaned_data["contact_person_name"]
        profile_created_by = self.cleaned_data["profile_created_by"]

        if profile_created_by != "SE" and not contact_person_name:
            raise forms.ValidationError(_("Contact person name is required"))
        else:
            contact_person_name = self.cleaned_data["name"]
        return contact_person_name

    def save(self, *args, **kwargs):
        user = super().save(*args, **kwargs)
        user.phone = self.cleaned_data["phone"]
        user.name = self.cleaned_data["name"]
        user.is_matrimony_candidate = True
        user.is_matrimony_registration_complete = False
        user.save()
        profile = MatrimonyProfile(
            user=user,
            email=user.email,
            name=self.cleaned_data["name"],
            gender=self.cleaned_data["gender"],
            marital_status=self.cleaned_data["marital_status"],
            phone=self.cleaned_data["phone"],
            dob=self.cleaned_data["dob"],
            rounds_chanting=self.cleaned_data["rounds_chanting"],
            profile_created_by=self.cleaned_data["profile_created_by"],
            contact_person_name=self.cleaned_data["contact_person_name"],
        )
        profile.save()
        return user


class BaseMatrimonyProfileForm(forms.ModelForm):
    class Meta:
        model = MatrimonyProfile
        exclude = ["id"]

    def __init__(self, *args, **kwargs):
        self.wizard = kwargs.pop("wizard", False)
        super().__init__(*args, **kwargs)
        for field in self.Meta.readonly:
            self.fields[field].widget.attrs["readonly"] = True
            self.fields[field].disabled = True

        for field in self.Meta.required:
            self.fields[field].required = True


class MatrimonyProfileBasicDetailsForm(BaseMatrimonyProfileForm):
    dob = forms.DateField(
        label=_("Date of birth"),
        widget=forms.DateInput(
            format=("%b %d, %Y"),
            attrs={
                "class": "form-control datepicker",
                "data-provide": "datepicker",
                "data-date-format": "M dd, yyyy",
                "data-date-autoclose": "true",
            },
        ),
        input_formats=("%b %d, %Y",),
    )
    height = forms.DecimalField(
        min_value=90.00, max_value=250.00, help_text="Height in cms"
    )

    class Meta:
        model = MatrimonyProfile
        fields = (
            "name",
            "spiritual_name",
            "dob",
            "rounds_chanting",
            "spiritual_status",
            "spiritual_master",
            "ethnic_origin",
            "mother_tongue",
            "children_count",
            "height",
            "weight",
            "body_type",
            "complexion",
            "marital_status",
            "dob",
            "current_place",
            "current_city",
            "current_state",
            "current_country",
            "nationality",
            "personality",
            "recreational_activities",
            "devotional_services",
            "want_children",
            "medical_history",
        )
        required = [
            "rounds_chanting",
            "spiritual_status",
            "ethnic_origin",
            "mother_tongue",
            "height",
            "weight",
            "body_type",
            "complexion",
            "current_place",
            "nationality",
            "personality",
            "medical_history",
        ]
        readonly = [
            "name",
            "current_city",
            "current_state",
            "dob",
            "marital_status",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.marital_status == "UMR":
            self.fields["children_count"].widget = forms.HiddenInput()
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 md-3"),
                Column("spiritual_name", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column("dob", css_class="form-group col-md-6 md-3"),
                Column(
                    Field("ethnic_origin", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(
                Column(
                    Field("mother_tongue", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
                Column("rounds_chanting", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column(
                    Field(
                        "spiritual_status", css_class="select2", data_toggle="select2"
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field(
                        "spiritual_master", css_class="select2", data_toggle="select2"
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(
                Column("marital_status", css_class="form-group col-md-6 md-3"),
                Column("children_count", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column("height", css_class="form-group col-md-6 md-3"),
                Column("weight", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column(
                    Field("body_type", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field("complexion", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Field("current_place", css_class="form-control"),
            Row(
                Column("current_city", css_class="form-group col-md-6 md-3"),
                Column("current_state", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column(
                    Field(
                        "current_country", css_class="select2", data_toggle="select2"
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field("nationality", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            "personality",
            Row(
                Column("recreational_activities", css_class="form-group col-md-6 md-3"),
                Column("devotional_services", css_class="form-group col-md-6 md-3"),
            ),
            Field("want_children", csss_class="select2", data_toggle="select2"),
            "medical_history",
            Submit("submit", "Next" if self.wizard else "Save"),
        )

    def clean(self):
        super().clean()
        current_place = self.cleaned_data["current_place"]
        print(current_place, type(current_place[1]))
        if not (
            len(current_place) == 3
            and re.match("[\w ]+, [\w ]+(?:, [\w ]+)?", current_place[0])
            and current_place[1]
            and current_place[2]
        ):
            raise forms.ValidationError(_("Select a valid place from maps"))


class MatrimonyProfileReligionAndFamilyForm(BaseMatrimonyProfileForm):
    dob = forms.DateField(
        label=_("Date of birth"),
        widget=forms.DateInput(
            format=("%b %d, %Y"),
            attrs={
                "class": "form-control datepicker",
                "data-provide": "datepicker",
                "data-date-format": "M dd, yyyy",
                "data-date-autoclose": "true",
            },
        ),
        input_formats=("%b %d, %Y",),
    )
    mentor_1_name = forms.CharField(max_length=200)
    mentor_1_phone = forms.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
            )
        ],
    )
    mentor_1_email = forms.EmailField(required=False)

    mentor_2_name = forms.CharField(max_length=200, required=False)
    mentor_2_phone = forms.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r"^(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$"
            )
        ],
        required=False,
    )
    mentor_2_email = forms.EmailField(required=False)

    class Meta:
        model = MatrimonyProfile
        fields = (
            "religion",
            "caste",
            "caste_other",
            "subcaste",
            "subcaste_other",
            "dob",
            "tob",
            "birth_place",
            "birth_city",
            "birth_state",
            "birth_country",
            "are_parents_devotees",
            "family_values",
            "family_type",
            "family_status",
            "father_status",
            "mother_status",
            "brothers",
            "sisters",
            "brothers_married",
            "sisters_married",
            "family_location",
            "family_origin",
            "religious_background",
            "family_details",
        )
        required = [
            "religion",
            "birth_place",
            "are_parents_devotees",
            "family_type",
            "family_status",
            "father_status",
            "mother_status",
            "brothers",
            "sisters",
            "brothers_married",
            "sisters_married",
            "family_location",
        ]
        readonly = ["dob", "birth_city", "birth_state"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for n, mentor in enumerate(
            self.instance.mentors.all().order_by("created_at")[:2]
        ):
            self.fields["mentor_{}_name".format(n + 1)].initial = mentor.name
            self.fields["mentor_{}_phone".format(n + 1)].initial = mentor.phone
            self.fields["mentor_{}_email".format(n + 1)].initial = mentor.email
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                "Religous Information",
                Field("religion", css_class="select2", data_toggle="select2"),
                Row(
                    Column(
                        Field("caste", css_class="select2", data_toggle="select2"),
                        css_class="form-group col-md-6 md-3",
                    ),
                    Column("caste_other", css_class="form-group col-md-6 md-3"),
                ),
                Row(
                    Column(
                        Field("subcaste", css_class="select2", data_toggle="select2"),
                        css_class="form-group col-md-6 md-3",
                    ),
                    Column("subcaste_other", css_class="form-group col-md-6 md-3"),
                ),
                Row(
                    Column("dob", css_class="form-group col-md-6 md-3"),
                    Column(
                        Field(
                            "tob",
                            data_toggle="timepicker",
                            data_show_meridian="false",
                            data_default_time="false",
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                ),
                Field("birth_place", css_class="form-control"),
                Row(
                    Column("birth_city", css_class="form-group col-md-6 md-3"),
                    Column("birth_state", css_class="form-group col-md-6 md-3"),
                ),
                Field("birth_country", css_class="select2", data_toggle="select2"),
                "religious_background",
            ),
            Fieldset(
                "Family details",
                Row(
                    Column(
                        Field(
                            "are_parents_devotees",
                            css_class="select2",
                            data_toggle="select2",
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                    Column(
                        Field(
                            "family_values", css_class="select2", data_toggle="select2"
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                ),
                Row(
                    Column(
                        Field(
                            "family_type", css_class="select2", data_toggle="select2"
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                    Column(
                        Field(
                            "family_status", css_class="select2", data_toggle="select2"
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                ),
                Row(
                    Column(
                        Field(
                            "father_status", css_class="select2", data_toggle="select2"
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                    Column(
                        Field(
                            "mother_status", css_class="select2", data_toggle="select2"
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                ),
                Row(
                    Column("brothers", css_class="form-group col-md-6 md-3"),
                    Column("brothers_married", css_class="form-group col-md-6 md-3"),
                ),
                Row(
                    Column("sisters", css_class="form-group col-md-6 md-3"),
                    Column("sisters_married", css_class="form-group col-md-6 md-3"),
                ),
                Row(
                    Column(
                        Field(
                            "family_location",
                            css_class="select2",
                            data_toggle="select2",
                        ),
                        css_class="form-group col-md-6 md-3",
                    ),
                    Column("family_origin", css_class="form-group col-md-6 md-3"),
                ),
                "family_details",
            ),
            Fieldset(
                "Mentors",
                "mentor_1_name",
                Row(
                    Column("mentor_1_phone", css_class="form-group col-md-6 md-3"),
                    Column("mentor_1_email", css_class="form-group col-md-6 md-3"),
                ),
                "mentor_2_name",
                Row(
                    Column("mentor_2_phone", css_class="form-group col-md-6 md-3"),
                    Column("mentor_2_email", css_class="form-group col-md-6 md-3"),
                ),
            ),
            Submit("submit", "Next" if self.wizard else "Save"),
        )

    def clean(self):
        super().clean()
        birth_place = self.cleaned_data["birth_place"]
        print(birth_place, type(birth_place[1]))
        if not (
            len(birth_place) == 3
            and re.match("[\w ]+, [\w ]+(?:, [\w ]+)?", birth_place[0])
            and birth_place[1]
            and birth_place[2]
        ):
            raise forms.ValidationError(_("Select a valid place from maps"))
        brothers_married = self.cleaned_data["brothers_married"]
        brothers = self.cleaned_data["brothers"]
        sisters_married = self.cleaned_data["sisters_married"]
        sisters = self.cleaned_data["sisters"]

        if brothers_married > brothers:
            raise forms.ValidationError(
                _("Brothers married cannot be greater than number of brothers")
            )
        if sisters_married > sisters:
            raise forms.ValidationError(
                _("Sisters married cannot be greater than number of sisters")
            )

    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)
        mentors = obj.mentors.all().order_by("created_at")
        mentors_count = len(mentors)
        print("mentors", mentors)

        if mentors_count > 0:
            mentor = mentors[0]
            mentor.name = self.cleaned_data["mentor_1_name"]
            mentor.phone = self.cleaned_data["mentor_1_phone"]
            mentor.email = self.cleaned_data["mentor_1_email"]
            mentor.save()
        else:
            obj.mentors.create(
                name=self.cleaned_data["mentor_1_name"],
                phone=self.cleaned_data["mentor_1_phone"],
                email=self.cleaned_data["mentor_1_email"],
            )

        if mentors_count > 1:
            mentor = mentors[1]
            mentor.name = self.cleaned_data["mentor_2_name"]
            mentor.phone = self.cleaned_data["mentor_2_phone"]
            mentor.email = self.cleaned_data["mentor_2_email"]
            mentor.save()
        elif self.cleaned_data.get("mentor_2_name"):
            obj.mentors.create(
                name=self.cleaned_data["mentor_2_name"],
                phone=self.cleaned_data["mentor_2_phone"],
                email=self.cleaned_data["mentor_2_email"],
            )


class MatrimonyProfileProfessionalInfoForm(BaseMatrimonyProfileForm):
    class Meta:
        model = MatrimonyProfile
        fields = (
            "education",
            "education_details",
            "institution",
            "employed_in",
            "occupations",
            "occupation_details",
            "organization",
            "annual_income",
        )
        required = ["employed_in", "education"]
        readonly = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field(
                "occupations",
                css_class="select2 form-control select2-multiple",
                data_toggle="select2",
                multiple="multiple",
            ),
            Row(
                Column(
                    Field("employed_in", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
                Column("organization", css_class="form-group col-md-6 md-3"),
            ),
            "annual_income",
            "occupation_details",
            Field(
                "education",
                css_class="select2 form-control select2-multiple",
                data_toggle="select2",
                multiple="multiple",
            ),
            Row(Column("institution", css_class="form-group col-md-6 md-3"),),
            "education_details",
            Submit("submit", "Next" if self.wizard else "Save"),
        )


class MatrimonyProfilePhotosForm(forms.Form):

    photos_visible_to_all_matches = forms.BooleanField(
        required=False,
        help_text="By default, your photos will be visible to all suggested matches. If you uncheck this option, your photos will only be visible to matches you have accepted.",
    )

    class Meta:
        model = MatrimonyProfile
        fields = ("photos_visible_to_all_matches",)
        readonly = []
        required = []

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        self.wizard = kwargs.pop("wizard")
        super().__init__(*args, **kwargs)
        self.fields[
            "photos_visible_to_all_matches"
        ].initial = self.instance.photos_visible_to_all_matches
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "photos_visible_to_all_matches",
            Submit("submit", "Next" if self.wizard else "Save"),
        )
        self.fields.required = True

    def save(self, *args, **kwargs):
        self.instance.photos_visible_to_all_matches = self.cleaned_data[
            "photos_visible_to_all_matches"
        ]
        self.instance.save()

    def clean(self):
        """Check that at least one photo has been entered."""
        super().clean()
        if not any(self.instance.photo_set.all()):
            raise forms.ValidationError(
                "Please upload at least a single photo to proceed."
            )


class MatrimonyProfileExpectationsForm(BaseMatrimonyProfileForm):

    age_from = forms.IntegerField(min_value=18, max_value=50)
    age_to = forms.IntegerField(min_value=18, max_value=50)
    height_from = forms.DecimalField(
        min_value=90.00, max_value=250.00, help_text="in cms"
    )
    height_to = forms.DecimalField(
        min_value=90.00, max_value=250.00, help_text="in cms"
    )

    class Meta:
        model = Expectation
        exclude = [
            "id",
            "profile",
            "annual_income_from_in_base_currency",
            "annual_income_to_in_base_currency",
        ]
        readonly = []
        required = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("age_from", css_class="form-group col-md-6 md-3"),
                Column("age_to", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column("height_from", css_class="form-group col-md-6 md-3"),
                Column("height_to", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column(
                    Field(
                        "religions",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field(
                        "mother_tongues",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(
                Column(
                    Field(
                        "castes",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field(
                        "subcastes",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(
                Column(
                    Field(
                        "countries_living_in",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field(
                        "ethnicities",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(
                Column("marital_status", css_class="form-group col-md-6 md-3"),
                Column("want_nri", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column(
                    Field(
                        "languages_can_speak",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field(
                        "languages_can_read_write",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(
                Column(
                    Field(
                        "education",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field(
                        "occupations",
                        css_class="select2 form-control select2-multiple",
                        data_toggle="select2",
                        multiple="multiple",
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(Column("employed_in", css_class="form-group col-md-6 md-3")),
            "annual_income_from",
            "annual_income_to",
            Row(
                Column("spiritual_status", css_class="form-group col-md-6 md-3"),
                Column("min_rounds_chanting", css_class="form-group col-md-6 md-3"),
            ),
            Field(
                "spiritual_masters",
                css_class="select2 form-control select2-multiple",
                data_toggle="select2",
                multiple="multiple",
            ),
            "partner_description",
            Submit("submit", "Submit" if self.wizard else "Save"),
        )

        def clean_age_from(self):
            value_from = self.cleaned_data["age_from"]
            value_to = self.cleaned_data["age_to"]
            if age_from > age_to:
                raise forms.ValidationError(_("From age should be less than to age"))

        def clean_height_from(self):
            value_from = self.cleaned_data["height_from"]
            value_to = self.cleaned_data["height_to"]
            if height_from > height_to:
                raise forms.ValidationError(
                    _("From height should be less than to height")
                )

        def save(self, *args, **kwargs):
            pass
