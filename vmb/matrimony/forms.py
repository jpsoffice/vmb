from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from allauth.account.forms import SignupForm as AllAuthSignupForm

from vmb.matrimony.models.profiles import (
    GENDER_CHOICES,
    MARITAL_STATUS,
    MatrimonyProfile,
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
