""" API v1 URLs. """

from django.urls import path, include, re_path
# from rest_framework import routers
#root_router = routers.DefaultRouter()
#root_router.register(r'bundles', BundleViewSet, basename='bundles')

from . import bundles, blocks, resources

app_name = 'v1'
urlpatterns = [
    path('bundles/<uuid:bundle_uuid>/', include([
        path('blocks/', bundles.bundle_blocks),
    ])),
    re_path(r'^blocks/(?P<usage_key_str>gblock-v1:[^/]+)/', include([
        path(r'', blocks.bundle_block, name='bundle-block'),
    ])),
    path('resource/<slug:block_type>/<path:path>', resources.xblock_resource, name='xblock-resource-url'),
]
