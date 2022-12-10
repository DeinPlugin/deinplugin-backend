# add a router
from rest_framework import routers
from django.urls import path, include

from .views import PluginViewSet

router = routers.DefaultRouter()
router.register(r'plugins', PluginViewSet)

# add a path

urlpatterns = [
    path('', include(router.urls)),
]
