"""
API Client for Blockstore bundle API
"""
from collections import namedtuple
from uuid import UUID

from django.conf import settings
import requests

Bundle = namedtuple('Bundle', ['uuid', 'title', 'slug'])
BundleFile = namedtuple('BundleFile', ['path', 'size', 'data_url'])


def api_url(*path_parts):
    if not settings.BLOCKSTORE_API_URL.endswith('/api/v1/'):
        raise ValueError('BLOCKSTORE_API_URL must end with /api/v1/')
    return settings.BLOCKSTORE_API_URL + '/'.join(path_parts) + '/'


def get_bundle(bundle_uuid: UUID):
    """
    Retrieve metadata about the specified bundle

    Returns None if the bundle does not exist
    """
    assert isinstance(bundle_uuid, UUID)
    response = requests.get(api_url('bundles', str(bundle_uuid)))
    if response.status_code == 404:
        return None
    response.raise_for_status()
    data = response.json()
    return Bundle(uuid=bundle_uuid, title=data['title'], slug=data['slug'])


def get_bundle_files(bundle_uuid: UUID):
    """
    Retrieve the list of files in the specified bundle
    """
    assert isinstance(bundle_uuid, UUID)
    files_response = requests.get(api_url('bundles', str(bundle_uuid), 'files'))
    files_response.raise_for_status()
    files_data = files_response.json()
    files = [
        BundleFile(path=f['path'], size=f['size'], data_url=f['data'])
        for f in files_data
    ]
    return files


def get_bundle_file_metadata(bundle_uuid: UUID, path: str):
    """
    Get the metadata of the specified file.
    """
    assert isinstance(bundle_uuid, UUID)
    # TODO: the following URL needs a weird double // ("".../files//file.xml")
    response = requests.get(api_url('bundles', str(bundle_uuid), 'files', path))
    response.raise_for_status()
    file_metadata = response.json()
    return BundleFile(
        path=file_metadata['path'],
        size=file_metadata['size'],
        data_url=file_metadata['data'],
    )


def get_bundle_file_data(bundle_uuid: UUID, path: str):
    """
    Read all the data in the given bundle file and return it as a
    binary string.

    Do not use this for large files!
    """
    metadata = get_bundle_file_metadata(bundle_uuid, path)
    with requests.get(metadata.data_url, stream=True) as r:
        return r.content
