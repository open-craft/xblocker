"""
Setup script for XBlocker
"""

from setuptools import setup

setup(
    name="XBlocker",
    version="0.1",
    install_requires=["setuptools"],
    requires=[],
    packages=[
        "xblocker",
    ],
    entry_points={
        'definition_key': [
            'olx-v1 = xblocker.lib.xblock_keys.bundle_def:BundleDefinitionLocator',
        ],
        'context_key': [
            'gcl = xblocker.lib.xblock_keys.learning_context_key:GlobalContextLocator',
        ],
        'usage_key': [
            'gblock-v1 = xblocker.lib.xblock_keys.usage_locator:GlobalUsageLocator',
        ],

    }
)
