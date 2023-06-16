from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from miraki.users.api.views import UserViewSet
from miraki.apps.hub_tenant.views import *

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("userprofiles", UserProfileViewSet)
router.register("sites", SiteViewSet)
router.register("areas", AreaViewSet)
router.register("lines", LineViewSet)
router.register("processes", ProcessViewSet)
router.register("machines", MachineViewSet)
router.register("tags", TagTopicsViewSet)


app_name = "api"
urlpatterns = router.urls
