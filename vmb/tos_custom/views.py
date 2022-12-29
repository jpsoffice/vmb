from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tos.views import *


def _redirect_to(redirect_to):
    """ Moved redirect_to logic here to avoid duplication in views"""

    # Light security check -- make sure redirect_to isn't garbage.
    if not redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL

    # Heavier security check -- redirects to http://example.com should
    # not be allowed, but things like /view/?param=http://example.com
    # should be allowed. This regex checks if there is a '//' *before* a
    # question mark.
    elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
            redirect_to = settings.LOGIN_REDIRECT_URL
    return redirect_to


@csrf_protect
@never_cache
def check_tos(request, template_name='tos/tos_check.html',
              redirect_field_name=REDIRECT_FIELD_NAME,):
    print("Hello")
    redirect_to = _redirect_to(request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, '')))
    tos = TermsOfService.objects.get_current_tos()
    if request.method == "POST":
        if request.POST.get("accept", "") == "accept":
            user = get_user_model().objects.get(pk=request.session['tos_user'])
            user.backend = request.session['tos_backend']

            # Save the user agreement to the new TOS
            UserAgreement.objects.get_or_create(terms_of_service=tos, user=user)

            key_version = cache.get('django:tos:key_version')
            cache.delete(f'django:tos:agreed:{user.pk}', version=key_version)

            # Log the user in
            auth_login(request, user)

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            return HttpResponseRedirect(redirect_to)
        else:
            messages.error(
                request,
                _("You cannot login without agreeing to the terms of this site.")
            )
            return HttpResponseRedirect(reverse('account_logout'))
    context = {
        'tos': tos,
        'redirect_field_name': redirect_field_name,
        'next': redirect_to,
    }
    return render(request, template_name, context)