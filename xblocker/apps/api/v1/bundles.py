"""
Views for dealing with XBlocks that are in a Blockstore bundle.
"""
from uuid import UUID

from django.http import Http404, JsonResponse
from django.urls import reverse
import six

from xblocker.lib.blockstore_api import get_bundle, list_olx_definitions
from xblocker.lib.xblock_keys import global_context, BundleDefinitionLocator


def bundle_blocks(request, bundle_uuid: UUID):
    """
    List all the block definitions in the specified bundle.
    """
    bundle = get_bundle(bundle_uuid)
    if bundle is None:
        raise Http404("Bundle not found")

    data = list_olx_definitions(bundle_uuid)
    result = []
    for path, entries in six.viewitems(data):
        blocks = []
        for (block_type, definition_id) in entries:
            definition_key = BundleDefinitionLocator(
                bundle_uuid=bundle_uuid, block_type=block_type, definition_id=definition_id,
            )
            usage_key = global_context.make_usage_key(definition_key)
            blocks.append({
                "definition_key": six.text_type(definition_key),
                "url": request.build_absolute_uri(
                    reverse('xblocker_api:v1:bundle-block', kwargs={'usage_key_str': six.text_type(usage_key)})
                ),
            })
        result.append({
            "path": path,
            "blocks": blocks,
        })
    return JsonResponse({"bundle_files": result})
