"""
Views related to individual XBlocks
"""
from django.http import JsonResponse, HttpResponseBadRequest
import six
from xblock.exceptions import NoSuchViewError
from xblock.runtime import DictKeyValueStore

from opaque_keys.edx.keys import UsageKey
from xblocker.lib.xblock_runtime.blockstore_kvs import BlockstoreKVS, blockstore_transaction
from xblocker.lib.xblock_runtime.blockstore_runtime import BlockstoreXBlockRuntime
from xblocker.lib.xblock_runtime.runtime import XBlockRuntimeSystem
from xblocker.lib.xblock_keys import global_context


def get_blockstore_kvs():
    """
    Get the BlockstoreKVS singleton.

    This key-value store is used by the XBlock runtime's SplitFieldData
    class as the underlying data store for authored data. It reads and
    writes XML data from bundles in blockstore.
    """
    # pylint: disable=protected-access
    if not hasattr(get_blockstore_kvs, '_kvs'):
        get_blockstore_kvs._kvs = BlockstoreKVS()
    return get_blockstore_kvs._kvs


def get_user_state_kvs():
    """
    Get the key-value store used by the XBlock runtime's SplitFieldData
    class to hold user state.

    This user state is not persisted anywhere.
    """
    # pylint: disable=protected-access
    if not hasattr(get_user_state_kvs, '_kvs'):
        get_user_state_kvs._kvs = DictKeyValueStore()
    return get_user_state_kvs._kvs


def get_readonly_runtime_system():
    """
    Get the XBlockRuntimeSystem for viewing content in Studio but
    not editing it at the moment
    """
    # pylint: disable=protected-access
    if not hasattr(get_readonly_runtime_system, '_system'):
        get_readonly_runtime_system._system = XBlockRuntimeSystem(
            # TODO: Need an actual method for calling handler_urls with this runtime:
            handler_url=lambda *args, **kwargs: 'test_url',
            authored_data_kvs=get_blockstore_kvs(),
            student_data_kvs=get_user_state_kvs(),
            runtime_class=BlockstoreXBlockRuntime,
        )
    return get_readonly_runtime_system._system


def bundle_block(request, usage_key_str, view_name='student_view'):
    """
    Get the HTML, JS, and CSS needed to render the given XBlock
    in the global learning context
    """
    usage_key = UsageKey.from_string(usage_key_str)
    if usage_key.context_key != global_context:
        return HttpResponseBadRequest("This API method only works with usages in the global context.")

    fallback_view = None
    if view_name == 'author_view':
        fallback_view = 'student_view'

    runtime = get_readonly_runtime_system().get_runtime(user_id=request.user.id)
    with blockstore_transaction():
        block = runtime.get_block(usage_key)
        try:
            fragment = block.render(view_name)
        except NoSuchViewError:
            if fallback_view:
                fragment = block.render('student_view')
            else:
                raise

    data = {
        "usage_key": six.text_type(usage_key),
    }
    data.update(fragment.to_dict())

    return JsonResponse(data)
