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
def profile_edit(request, section_id):
    sections = [
        {
            "id": "basic",
            "label": "Basic",
            "form_class": MatrimonyProfileBasicDetailsForm,
            "path": reverse("matrimony:profile-edit", args=["basic"]),
        },
        {
            "id": "profession",
            "label": "Profession",
            "form_class": MatrimonyProfileProfessionalInfoForm,
            "path": reverse("matrimony:profile-edit", args=["profession"]),
        },
        {
            "id": "religion-and-family",
            "label": "Religion & Family",
            "form_class": MatrimonyProfileReligionAndFamilyForm,
            "path": reverse("matrimony:profile-edit", args=["religion-and-family"]),
        },
    ]
    sections_count = len(sections)
    section_id_index_map = {s["id"]: n for n, s in enumerate(sections)}

    if section_id not in section_id_index_map:
        raise Http404()

    section_index = section_id_index_map[section_id]
    section = sections[section_index]
    section["active"] = True

    try:
        matrimony_profile = MatrimonyProfile.objects.get(user=request.user)
    except MatrimonyProfile.DoesNotExist:
        raise Http404("Your matrimony profile does not exist.")

    wizard = False
    if not request.user.is_matrimony_registration_complete:
        wizard = True
    form = section["form_class"](instance=matrimony_profile, wizard=wizard)

    if request.method == "POST":
        form = section["form_class"](
            instance=matrimony_profile, data=request.POST, wizard=wizard
        )
        if form.is_valid():
            form.save()
            next = request.path_info
            if wizard and section_index + 1 < sections_count:
                next = sections[section_index + 1]["path"]
            else:
                next = "/"
                request.user.is_matrimony_registration_complete = True
                request.user.save()
            return HttpResponseRedirect(next)

    if wizard:
        for s in sections[section_index:]:
            s["path"] = "#"

    return render(
        request, "matrimony/profile_edit.html", {"form": form, "sections": sections}
    )
