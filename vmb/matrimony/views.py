import logging
import os
import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse
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
    SignupForm,
)

from actstream import action
from actstream.models import Action
from vmb.common import activities
from vmb.users.models import User

from django.core.paginator import Paginator

import traceback

def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("matrimony:profile-edit", args=["basic"]))
    else:
        form = SignupForm()
        return render(request, "landing.html", {"form": form})


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
                    action.send(request.user, verb=activities.USER_REGISTERED)
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
def matches(request, category=None):
    profile = get_object_or_404(MatrimonyProfile, email=request.user.email)
    if category == "suggested":
        matches = (
            profile.female_matches.filter(sender_gender=None)
            if profile.gender == "M"
            else profile.male_matches.filter(sender_gender=None)
        )
    elif category == "sent":
        matches = profile.matches.filter(sender_gender=profile.gender)
    elif category == "received":
        matches = profile.matches.filter(
            sender_gender="F" if profile.gender == "M" else "M"
        )
    else:
        return HttpResponseRedirect(reverse("matrimony:matches", args=["suggested"]))

    _matches = [
        {
            "id": m.id,
            "profile": m.male if profile.gender == "F" else m.female,
            "your_response": m.male_response
            if profile.gender == "M"
            else m.female_response,
            "response": m.male_response if profile.gender == "F" else m.female_response,
            "show_photo": m.female_photos_visibility
            if profile.gender == "M"
            else m.male_photos_visibility,
        }
        for m in matches
    ]

    return render(
        request, "matrimony/matches.html", {"category": category, "matches": _matches}
    )


@login_required
def search(request, page):
    profile = get_object_or_404(MatrimonyProfile, email=request.user.email)

    if profile.status < "20":
        return render(
            request,
            "matrimony/search.html",
            {
                "search_disabled": True,
                "profiles": None,
                "search_form": None,
                "querydata": None,
                "email_contact": settings.EMAIL_CONTACT,
            },
        )

    expectations = profile.expectations
    form = MatrimonyProfileSearchForm(instance=expectations)
    profiles = []
    querydata = form.initial

    if request.method == "GET" and request.GET:
        form = MatrimonyProfileSearchForm(request.GET)
        if not form.is_valid():
            logging.debug("profile search form errors: {}".format(form.errors))
            return render(
                request, "matrimony/search.html", {"profiles": [], "search_form": form}
            )
        profiles = profile.search_profiles(form.cleaned_data)
        logging.debug("search profile results: {}".format((profiles)))
        querydata = form.cleaned_data
    else:
        profiles = profile.search_profiles()
        logging.debug("search profile results: {}".format((profiles)))

    pages = Paginator(profiles, per_page=settings.MATCH_SEARCH_PAGE_SIZE)
    context = {
        "profiles": pages.page(page),
        "search_form": form,
        "querydata": form.humanized_data(),
        "num_pages": pages.num_pages+1,
        "active_page": pages.page(page)
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
        if action == "accept":
            globals()['action'].send(request.user, verb=activities.MATCH_REQUEST_ACCEPTED, target=match.female.user)
        else:
            globals()['action'].send(request.user, verb=activities.MATCH_REQUEST_REJECTED, target=match.female.user)
    else:
        match.female_response = action_code
        match.female_response_updated_at = timezone.now()
        if action == "accept":
            globals()['action'].send(request.user, verb=activities.MATCH_REQUEST_ACCEPTED, target=match.male.user)
        else:
            globals()['action'].send(request.user, verb=activities.MATCH_REQUEST_REJECTED, target=match.male.user)
    match.save()

    return JsonResponse(data={})


@require_http_methods(["POST"])
@login_required
def match_create(request, profile_id):
    profile = request.user.matrimony_profile

    recipient_profile = get_object_or_404(
        MatrimonyProfile,
        profile_id=profile_id,
        gender="M" if profile.gender == "F" else "F",
    )

    defaults = {
        "sender_gender": profile.gender,
        "category": "USR",
        "created_by": request.user,
        "updated_by": request.user,
    }
    kwargs = {
        "male": profile if profile.gender == "M" else recipient_profile,
        "female": recipient_profile if profile.gender == "M" else profile,
        "defaults": defaults,
    }
    match, created = Match.objects.get_or_create(**kwargs)

    response_data = {}

    if created:
        action.send(request.user, verb=activities.MATCH_REQUEST_SENT, target=recipient_profile)
        messages.add_message(
            request,
            messages.SUCCESS,
            "Match request sent. You can view 'Sent' tab in your Matches page",
        )
    else:
        messages.add_message(
            request,
            messages.ERROR,
            "A match already exists under '{}' tab in your Matches page".format(
                "Suggested" if match.sender_gender is None else "Received"
            ),
        )

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


@login_required
def mark_as_read(request, pk):
    required_notification = request.user.notifications.get(id=pk)
    required_notification.unread = False
    required_notification.save()
    return redirect(request.META["HTTP_REFERER"])


@login_required
def mark_all_as_read(request):
    required_notifications = request.user.notifications.unread().all
    required_notification_objects = required_notifications().all()
    for notification_object in required_notification_objects:
        notification_object.unread = False
        notification_object.save()
    return redirect(request.META["HTTP_REFERER"])


@login_required
def view_all_notifications(request):
    return render(request, "matrimony/view_all_notifications.html")

@login_required
def view_timeline(request):
    try:
        return render(request, "actstream/view_timeline.html")
    except Exception as e:
        print(traceback.format_exc())
        print(str(e))