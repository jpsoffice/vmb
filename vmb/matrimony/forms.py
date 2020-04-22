from django import forms
from django.utils.translation import ugettext_lazy as _


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
