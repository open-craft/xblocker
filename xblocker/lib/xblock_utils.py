"""
Helper methods for working with XBlocks
"""
from django.urls import reverse

def xblock_local_resource_url(block, uri):
    """
    Returns the URL for an XBlock's local resource.
    """
    # Todo: in production, serve this via a CDN
    # if settings.PIPELINE_ENABLED or not settings.REQUIRE_DEBUG:
    #     xblock_class = getattr(block.__class__, 'unmixed_class', block.__class__)
    #     return staticfiles_storage.url('xblock/resources/{package_name}/{path}'.format(
    #         package_name=xblock_resource_pkg(xblock_class),
    #         path=uri
    #     ))
    return reverse('xblocker_api:v1:xblock-resource-url', kwargs={
        'block_type': block.scope_ids.block_type,
        'path': uri,
    })


def xblock_resource_pkg(block):
    """
    Return the module name needed to find an XBlock's shared static assets.

    This method will return the full module name that is one level higher than
    the one the block is in. For instance, problem_builder.answer.AnswerBlock
    has a __module__ value of 'problem_builder.answer'. This method will return
    'problem_builder' instead. However, for edx-ora2's
    openassessment.xblock.openassessmentblock.OpenAssessmentBlock, the value
    returned is 'openassessment.xblock'.
    """
    return block.__module__.rsplit('.', 1)[0]
