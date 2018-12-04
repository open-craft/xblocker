"""
Root API URLs.

All API URLs should be versioned, so urlpatterns should only
contain namespaces for the active versions of the API.
"""
from django.urls import path, include

app_name = 'xblocker_api'
urlpatterns = [
    path('v1/', include('xblocker.apps.api.v1.urls')),
]
