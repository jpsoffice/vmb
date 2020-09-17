from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from vmb.matrimony.models import MatrimonyProfile
from vmb.matrimony.forms import (
    MatrimonyProfileBasicDetailsForm,
    MatrimonyProfileProfessionalInfoForm,
    MatrimonyProfileReligionAndFamilyForm,
)


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("matrimony:profile-edit", args=["basic"]))
    else:
        return HttpResponseRedirect(reverse("account_login"))


@login_required
def profile_edit(request, section):
    if section == "basic":
        form_class = MatrimonyProfileBasicDetailsForm
    elif section == "religion-and-family":
        form_class = MatrimonyProfileReligionAndFamilyForm
    elif section == "profession":
        form_class = MatrimonyProfileProfessionalInfoForm
    else:
        raise Http404()

    try:
        matrimony_profile = MatrimonyProfile.objects.get(user=request.user)
    except MatrimonyProfile.DoesNotExist:
        raise Http404("Your matrimony profile does not exist.")
    form = form_class(instance=matrimony_profile)
    if request.method == "POST":
        form = form_class(instance=matrimony_profile, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path_info)
    return render(
        request, "matrimony/profile_edit.html", {"form": form, "section": section}
    )
