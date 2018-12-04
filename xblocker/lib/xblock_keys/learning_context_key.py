"""
Defines keys for "learning contexts" and the global learning context singleton.
"""
# Disable warnings about _to_deprecated_string etc. which we don't want to implement:
# pylint: disable=abstract-method
from opaque_keys import OpaqueKey, InvalidKeyError


class LearningContextKey(OpaqueKey):
    """
    A key that idenitifies a course, a library, a program,
    or some other collection of content where learning happens.
    """
    KEY_TYPE = 'context_key'
    __slots__ = ()

    def make_usage_key(self, definition_key, usage_id=None):
        """
        Return a usage key, given the given the specified definition key and usage_id
        This function should not actually create any new ids, but should simply
        return one that already exists.
        """
        raise NotImplementedError()


class GlobalContextLocator(LearningContextKey):
    """
    A key for the "global context", which means viewing some
    block definition directly (e.g. in a library/bundle) and
    not as part of a course or other context.

    Always serializes as "gcl:global"
    """
    CANONICAL_NAMESPACE = 'gcl'
    KEY_FIELDS = ()
    __slots__ = KEY_FIELDS
    CHECKED_INIT = False
    KEY_VALUE = 'global'

    def _to_string(self):
        return self.KEY_VALUE

    @classmethod
    def _from_string(cls, serialized):
        if serialized != cls.KEY_VALUE:
            raise InvalidKeyError(cls, serialized)
        return cls()

    def make_usage_key(self, definition_key, usage_id=None):
        """
        Return a usage key, given the given the specified definition key and usage_id
        This function should not actually create any new ids, but should simply
        return one that already exists.
        """
        if usage_id is not None:
            raise ValueError("Cannot have a usage_id in the global context")
        from .usage_locator import GlobalUsageLocator  # Avoid circular import
        return GlobalUsageLocator(definition_key)

global_context = GlobalContextLocator()
