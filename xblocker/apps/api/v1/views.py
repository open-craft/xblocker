"""
Main views of the bundles API
"""

from rest_framework.viewsets import ViewSet
from rest_framework.request import Request
from rest_framework.response import Response


class BundleViewSet(ViewSet):
    """
    Basic empty view
    """

    def list(self, request: Request) -> Response:  # pylint: disable=unused-argument
        return Response({'working': 'yes'})
