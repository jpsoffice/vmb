from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

# Django-notifications-hq imports
from django.conf.urls import url
import notifications.urls

# wagtail imports:
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from vmb.users.views import NewSignupView

from vmb.tos_custom.views import check_tos as custom_check_tos

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path("impersonate/", include("impersonate.urls")),
    # User management
    path("users/", include("vmb.users.urls", namespace="users")),
    path('accounts/signup/', NewSignupView.as_view(), name="new_signup"),
    path("accounts/", include("allauth.urls")),
    url('avatar/', include('avatar.urls')),
    path("photologue/", include("photologue.urls", namespace="photologue")),
    path("", include("vmb.matrimony.urls", namespace="matrimony")),
    path("tinymce/", include("tinymce.urls")),
    path("newsletter/", include("newsletter.urls")),
    url(
        "^inbox/notifications/", include(notifications.urls, namespace="notifications")
    ),
    # Wagtail URLs:
    path("cms/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("pages/", include(wagtail_urls)),
    path("wagtail/", include(wagtail_urls)),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path("terms-of-service/confirm/", custom_check_tos, name="tos_check_tos"),
    path("terms-of-service/", include("tos.urls")),
    path('activity/', include('actstream.urls')),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

# urlpatterns += [path('matrimony/', include('matrimony.urls'))]
