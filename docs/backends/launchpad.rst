Launchpad
=========

`Ubuntu Launchpad <https://launchpad.net/>`_ OpenID doesn't require
major settings beside being defined on ``AUTHENTICATION_BACKENDS```::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.launchpad.LaunchpadOpenId',
        ...
    )
