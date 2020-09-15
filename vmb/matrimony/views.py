from django.shortcuts import render, get_object_or_404

# from django.views.generic import ListView
from vmb.matrimony.models.profiles import MatrimonyProfile
from vmb.matrimony.models import Match

# Create your views here.
def match_response(request, id):

    profile_user = get_object_or_404(MatrimonyProfile, email=request.user.email)
    profile = get_object_or_404(MatrimonyProfile, id=id)

    if profile_user.gender == "M":
        match = get_object_or_404(Match, male=profile_user, female=profile)
        if request.POST:
            match.male_response = request.POST["response"]
            match.save()
        response = match.male_response
    else:
        match = get_object_or_404(Match, male=profile, female=profile_user)
        if request.POST:
            match.female_response = request.POST["response"]
            match.save()
        response = match.female_response

    context = {
        "m": profile,
        "response": response,
    }

    return render(request, "matrimony/match/response.html", context)
