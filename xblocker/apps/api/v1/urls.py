""" API v1 URLs. """

from django.urls import path, include
from rest_framework import routers

from .views import BundleViewSet

root_router = routers.DefaultRouter()

root_router.register(r'bundles', BundleViewSet, basename='bundles')

app_name = 'v1'
urlpatterns = [
    path('', include(root_router.urls)),
]
