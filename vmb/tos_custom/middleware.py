from tos.middleware import UserAgreementMiddleware
from django.conf import settings


class CustomUserAgreementMiddleware(UserAgreementMiddleware):

    def process_request(self, request):
        for path in settings.TOS_EXCLUDE_PATH_PREFIXES:
            if request.path.startswith(path):
                return None
        return super().process_request(request)