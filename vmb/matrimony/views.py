import os
import uuid

from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods

from photologue.models import Photo as PhotologuePhoto

from vmb.matrimony.models import MatrimonyProfile, Photo, Expectation, Match
from vmb.matrimony.forms import (
    MatrimonyProfileBasicDetailsForm,
    MatrimonyProfileProfessionalInfoForm,
    MatrimonyProfileReligionAndFamilyForm,
    MatrimonyProfilePhotosForm,
    MatrimonyProfileExpectationsForm,
    MatrimonyProfileSearchForm,
    ChangePasswordForm,
)


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("matrimony:profile-edit", args=["basic"]))
    else:
        return HttpResponseRedirect(reverse("account_login"))


@login_required
def profile_details(request, profile_id):
    profile = get_object_or_404(MatrimonyProfile, profile_id=profile_id)

    return render(
        request,
        "matrimony/profile_details.html",
        {
            "profile": profile,
            "show_personal_info": profile.is_personal_data_visible_to_user(
                request.user
            ),
        },
    )


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
        {
            "id": "expectations",
            "label": "Expectations",
            "form_class": MatrimonyProfileExpectationsForm,
            "path": reverse("matrimony:profile-edit", args=["expectations"]),
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

    instance = (
        matrimony_profile.expectations
        if section_id == "expectations"
        else matrimony_profile
    )
    form = section["form_class"](instance=instance, wizard=wizard)

    if request.method == "POST":
        form = section["form_class"](
            instance=instance, data=request.POST, wizard=wizard
        )
        if form.is_valid():
            obj = form.save()
            next = request.path_info
            if wizard:
                if section_index + 1 < sections_count:
                    next = sections[section_index + 1]["path"]
                else:
                    next = "/"
                    request.user.is_matrimony_registration_complete = True
                    matrimony_profile.set_status("Registered")
                    matrimony_profile.registration_date = timezone.now()
                    matrimony_profile.save()
                    request.user.save()
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        _("Thank you! Your registration has been submitted."),
                    )
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
def profile_photos_add(request):
    if request.POST:
        title = uuid.uuid5(uuid.uuid1(), str(os.getpid())).hex[:32]
        photologue_photo = PhotologuePhoto(
            image=request.FILES["file"], title=title, slug=title, is_public=True
        )
        photologue_photo.save()

        primary = False
        if Photo.objects.filter(profile=request.user.matrimony_profile).count() == 0:
            primary = True

        photo = Photo(
            photo=photologue_photo,
            profile=request.user.matrimony_profile,
            primary=primary,
        )
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


@login_required
def profile_photo_action(request, photo_id, action):
    if request.method == "POST":
        try:
            photo = request.user.matrimony_profile.photo_set.get(id=photo_id)
        except Photo.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Photo does not exist"}, status=404
            )
        if action == "make-primary":
            photo.primary = True
            photo.save()
        elif action == "delete":
            photo.photo.delete()
            photo.delete()
        else:
            return JsonResponse({}, status=404)
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"}, status=401)


@login_required
def matches(request):
    profile = get_object_or_404(MatrimonyProfile, email=request.user.email)
    context = {"matches_suggested": profile.matching_profiles_list}
    return render(request, "matrimony/matches.html", context)


@login_required
def search(request):
    profile = get_object_or_404(MatrimonyProfile, email=request.user.email)
    expectations = profile.expectations
    form = MatrimonyProfileSearchForm(instance=expectations)
    profiles = []
    querydata = form.initial

    if request.method == "GET" and request.GET:
        form = MatrimonyProfileSearchForm(request.GET)
        if not form.is_valid():
            return render(
                request, "matrimony/search.html", {"profiles": [], "search_form": form}
            )
        profiles = profile.search_profiles(form.cleaned_data)
        querydata = form.cleaned_data
    else:
        profiles = profile.search_profiles()

    context = {
        "profiles": profiles,
        "search_form": form,
        "querydata": form.humanized_data(),
    }
    return render(request, "matrimony/search.html", context)


@require_http_methods(["POST"])
@login_required
def match_action(request, id, action):
    profile = request.user.matrimony_profile
    matches = profile.matches.filter(id=id)
    if not matches:
        return Http404()

    if action not in ("accept", "reject"):
        return Http404()

    match = matches[0]

    action_code = "ACP" if action == "accept" else "REJ"
    if profile.gender == "M":
        match.male_response = action_code
        match.male_response_updated_at = timezone.now()
    else:
        match.female_response = action_code
        match.female_response_updated_at = timezone.now()
    match.save()

    return JsonResponse(data={})


@require_http_methods(["GET"])
@login_required
def match_details(request, id):
    profile = request.user.matrimony_profile
    if profile.gender == "M":
        match = get_object_or_404(Match, male_id=profile.id, id=id)
    else:
        match = get_object_or_404(Match, female_id=profile.id, id=id)
    match_profile = match.female if profile.gender == "M" else match.male
    response = match.male_response if profile.gender == "M" else match.female_response
    match_response = (
        match.female_response if profile.gender == "M" else match.male_response
    )
    show_photo = (
        match.show_female_photos if profile.gender == "M" else match.show_male_photos
    )

    return render(
        request,
        "matrimony/match_details.html",
        {
            "profile": profile,
            "match": match,
            "match_profile": match_profile,
            "response": response,
            "match_response": match_response,
            "show_photo": show_photo,
        },
    )

