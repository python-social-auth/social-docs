AOL
===

AOL OpenID doesn't require major settings beside being defined on
``AUTHENTICATION_BACKENDS```::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.aol.AOLOpenId',
        ...
    )
