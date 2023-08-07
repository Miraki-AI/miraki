from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from miraki.apps.hub_tenant.views import *
from miraki.apps.customers.views import TenantApiView

urlpatterns = [
    path("core", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path("core/about/", TemplateView.as_view(template_name="pages/about.html"), name="about"),
    # Django Admin, use {% url 'admin:index' %}
    path("core/"+settings.ADMIN_URL, admin.site.urls),
    # User management
    path("core/users/", include("miraki.users.urls", namespace="users")),
    path("core/accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("core/api/", include("config.api_router")),
    # DRF auth token
    path("core/auth-token/", obtain_auth_token),
    path("core/login/", CustomAuthToken.as_view()),
    
    path("core/api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "core/api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

# APP API URLS
urlpatterns += [
    path("core/api/new-tenant/", TenantApiView.as_view(), name="new-tenant" ),
    # path("core/api/user-onboard/", UserOnboardApi.as_view(), name="user-onboard" ),
    path("core/api/invite-user/", InviteUserApi.as_view(), name="invite-user" ),
    path("core/api/is-user-exists/", IsUserExists.as_view(), name="is-user-exists" ),
    path("core/api/onboard-user/", UserOnboardApi.as_view(), name="onboard-user" ),
    path("core/api/process-choices/", ProcessChoicesView.as_view(), name="process-choices" ),
    
    
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "core/400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "core/403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "core/404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
