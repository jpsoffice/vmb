import os
import uuid

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from photologue.models import Photo as PhotologuePhoto

from vmb.matrimony.models import MatrimonyProfile, Photo
from vmb.matrimony.forms import (
    MatrimonyProfileBasicDetailsForm,
    MatrimonyProfileProfessionalInfoForm,
    MatrimonyProfileReligionAndFamilyForm,
    MatrimonyProfilePhotosForm,
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
        {
            "id": "photos",
            "label": "Photos",
            "form_class": MatrimonyProfilePhotosForm,
            "path": reverse("matrimony:profile-edit", args=["photos"]),
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
        print(request.FILES)
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
        request,
        "matrimony/profile_edit.html",
        {"form": form, "section_id": section_id, "sections": sections},
    )


@login_required
def profile_photos_ajax(request):
    if request.POST:
        title = uuid.uuid5(uuid.uuid1(), str(os.getpid())).hex[:32]
        photologue_photo = PhotologuePhoto(
            image=request.FILES["file"], title=title, slug=title, is_public=True
        )
        photologue_photo.save()
        photo = Photo(photo=photologue_photo, profile=request.user.matrimony_profile)
        photo.save()
        return JsonResponse(
            {
                "error": False,
                "data": {
                    "image_url": photo.photo.get_display_url(),
                    "thumbnail_url": photo.photo.get_thumbnail_url(),
                    "id": photo.id,
                    "title": photo.photo.title,
                    "slug": photo.photo.slug,
                },
            }
        )
