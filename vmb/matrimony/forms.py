from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from allauth.account.forms import SignupForm as AllAuthSignupForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Field, Submit

from multiselectfield import MultiSelectFormField

from vmb.matrimony.models.profiles import (
    GENDER_CHOICES,
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
    phone = forms.CharField(min_length=10, max_length=17)
    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={"class": "form-control", "data-provide": "datepicker"}
        )
    )
    rounds_chanting = forms.IntegerField(min_value=1, max_value=192)

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

        for field in self.Meta.required:
            self.fields[field].required = True


class MatrimonyProfileBasicDetailsForm(BaseMatrimonyProfileForm):
    class Meta:
        model = MatrimonyProfile
        fields = (
            "name",
            "spiritual_name",
            "rounds_chanting",
            "spiritual_status",
            "spiritual_master",
            "ethnic_origin",
            "mother_tongue",
            "marital_status",
            "children_count",
            "height",
            "weight",
            "body_type",
            "complexion",
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
            "marital_status",
            "height",
            "weight",
            "body_type",
            "complexion",
            "current_place",
            "nationality",
            "personality",
            "medical_history",
        ]
        readonly = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.marital_status == "UMR":
            self.fields.pop("children_count")
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column("name", css_class="form-group col-md-6 md-3"),
                Column("spiritual_name", css_class="form-group col-md-6 md-3"),
            ),
            Row(
                Column(
                    Field("ethnic_origin", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field("mother_tongue", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Row(
                Column("rounds_chanting", css_class="form-group col-md-6 md-3"),
                Column(
                    Field(
                        "spiritual_status", css_class="select2", data_toggle="select2"
                    ),
                    css_class="form-group col-md-6 md-3",
                ),
            ),
            Field("spiritual_master", css_class="select2", data_toggle="select2"),
            Row(
                Column(
                    Field("marital_status", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
                Column(
                    Field("children_count", css_class="select2", data_toggle="select2"),
                    css_class="form-group col-md-6 md-3",
                ),
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


class MatrimonyProfileReligionAndFamilyForm(BaseMatrimonyProfileForm):
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
            "subcaste",
            "dob",
            "tob",
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
        readonly = []

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
                    Column(
                        Field("subcaste", css_class="select2", data_toggle="select2"),
                        css_class="form-group col-md-6 md-3",
                    ),
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
            "annual_income",
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
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance")
        self.wizard = kwargs.pop("wizard")
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Submit("submit", "Next" if self.wizard else "Save"),
        )

    def save(self, *args, **kwargs):
        pass


class MatrimonyProfileExpectationsForm(BaseMatrimonyProfileForm):
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
