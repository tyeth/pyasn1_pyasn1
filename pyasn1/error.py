#
# This file is part of pyasn1 software.
#
# Copyright (c) 2005-2020, Ilya Etingof <etingof@gmail.com>
# License: https://pyasn1.readthedocs.io/en/latest/license.html
#

import sys

class PyAsn1Error(Exception):
    """Base pyasn1 exception

    `PyAsn1Error` is the base exception class (based on
    :class:`Exception`) that represents all possible ASN.1 related
    errors.

    Parameters
    ----------
    args:
        Opaque positional parameters

    Keyword Args
    ------------
    kwargs:
        Opaque keyword parameters

    """
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs

    @property
    def context(self):
        """Return exception context

        When exception object is created, the caller can supply some opaque
        context for the upper layers to better understand the cause of the
        exception.

        Returns
        -------
        : :py:class:`dict`
            Dict holding context specific data
        """
        return self._kwargs.get('context', {})


class ValueConstraintError(PyAsn1Error):
    """ASN.1 type constraints violation exception

    The `ValueConstraintError` exception indicates an ASN.1 value
    constraint violation.

    It might happen on value object instantiation (for scalar types) or on
    serialization (for constructed types).
    """


class SubstrateUnderrunError(PyAsn1Error):
    """ASN.1 data structure deserialization error

    The `SubstrateUnderrunError` exception indicates insufficient serialised
    data on input of a de-serialization codec.
    """


class EndOfStreamError(SubstrateUnderrunError):
    """ASN.1 data structure deserialization error

    The `EndOfStreamError` exception indicates the condition of the input
    stream has been closed.
    """


class UnsupportedSubstrateError(PyAsn1Error):
    """Unsupported substrate type to parse as ASN.1 data."""


# Check if we're running on CircuitPython which has stricter multiple inheritance rules
_IS_CIRCUITPYTHON = hasattr(sys, 'implementation') and sys.implementation.name == 'circuitpython'

if _IS_CIRCUITPYTHON:
    # CircuitPython-compatible versions without multiple inheritance from built-in exception types
    class PyAsn1UnicodeError(PyAsn1Error):
        """Unicode text processing error

        The `PyAsn1UnicodeError` exception is a base class for errors relating to
        unicode text de/serialization.

        Note: In CircuitPython, this only inherits from PyAsn1Error due to 
        multiple inheritance limitations.
        """
        def __init__(self, message, unicode_error=None):
            if unicode_error is not None:
                # Store unicode error info without multiple inheritance
                self.unicode_error = unicode_error
            PyAsn1Error.__init__(self, message)

    class PyAsn1UnicodeDecodeError(PyAsn1UnicodeError):
        """Unicode text decoding error

        The `PyAsn1UnicodeDecodeError` exception represents a failure to
        deserialize unicode text.

        Note: In CircuitPython, this only inherits from PyAsn1UnicodeError due to 
        multiple inheritance limitations.
        """

    class PyAsn1UnicodeEncodeError(PyAsn1UnicodeError):
        """Unicode text encoding error

        The `PyAsn1UnicodeEncodeError` exception represents a failure to
        serialize unicode text.

        Note: In CircuitPython, this only inherits from PyAsn1UnicodeError due to 
        multiple inheritance limitations.
        """

else:
    # Standard Python versions with full multiple inheritance support
    class PyAsn1UnicodeError(PyAsn1Error, UnicodeError):
        """Unicode text processing error

        The `PyAsn1UnicodeError` exception is a base class for errors relating to
        unicode text de/serialization.

        Apart from inheriting from :class:`PyAsn1Error`, it also inherits from
        :class:`UnicodeError` to help the caller catching unicode-related errors.
        """
        def __init__(self, message, unicode_error=None):
            if isinstance(unicode_error, UnicodeError):
                UnicodeError.__init__(self, *unicode_error.args)
            PyAsn1Error.__init__(self, message)

    class PyAsn1UnicodeDecodeError(PyAsn1UnicodeError, UnicodeDecodeError):
        """Unicode text decoding error

        The `PyAsn1UnicodeDecodeError` exception represents a failure to
        deserialize unicode text.

        Apart from inheriting from :class:`PyAsn1UnicodeError`, it also inherits
        from :class:`UnicodeDecodeError` to help the caller catching unicode-related
        errors.
        """

    class PyAsn1UnicodeEncodeError(PyAsn1UnicodeError, UnicodeEncodeError):
        """Unicode text encoding error

        The `PyAsn1UnicodeEncodeError` exception represents a failure to
        serialize unicode text.

        Apart from inheriting from :class:`PyAsn1UnicodeError`, it also inherits
        from :class:`UnicodeEncodeError` to help the caller catching
        unicode-related errors.
        """