from django.shortcuts import render, get_object_or_404
from vmb.matrimony.models.profiles import MatrimonyProfile
from vmb.matrimony.models import Match

# Create your views here.
def response(request, id):
    profile_user = get_object_or_404(MatrimonyProfile, email=request.user.email)
    profile = get_object_or_404(MatrimonyProfile, id=id)
    gender = profile_user.gender
    if gender == "M":
        match = get_object_or_404(Match, male=profile_user, female=profile)
        print(match.male, match.female)
        match_with_profile = match.female
        print(type(match_with_profile))
    else:
        match = get_object_or_404(Match, male=profile, female=profile_user)
        match_with_profile = match.male
    print(match)
    context = {
        "match_id": match.id,
        "m": match_with_profile,
    }
    print(context)
    return render(request, "matrimony/match/response.html", context)


def match(request, id):
    mp = get_object_or_404(MatrimonyProfile, email=request.user.email)
    match = get_object_or_404(Match, id=id)
    print(match)
    if mp.gender == "M":
        match.male_response = request.POST["response"]
        response = match.get_male_response_display()
        profile = match.female
    else:
        match.female_response = request.POST["response"]
        response = match.get_female_response_display()
        profile = match.male
    match.save()
    context = {
        "match_with_profile": profile,
        "response": response,
    }
    return render(request, "matrimony/match/match.html", context)
