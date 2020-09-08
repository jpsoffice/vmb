from django.shortcuts import render, get_object_or_404
from vmb.matrimony.models.profiles import MatrimonyProfile
from vmb.matrimony.models import Match

# Create your views here.
def response(request, id):
    mp = get_object_or_404(MatrimonyProfile, id=id)
    context = {
        "profile": mp,
    }
    return render(request, "matrimony/emails/response.html", context)


def accept_or_reject(request, id):
    mp = get_object_or_404(MatrimonyProfile, email=request.user.email)
    if mp.gender == "M":
        match = get_object_or_404(Match, male=mp.id, female=id)
        match.male_response = request.POST["response"]
    else:
        match = get_object_or_404(Match, male=id, female=mp.id)
        match.female_response = request.POST["response"]
    match.save()
    context = {
        "match": match,
        "gender": mp.gender,
    }
    return render(request, "matrimony/emails/accept_or_reject.html", context)
