Launchpad
=========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``launchpad``
     - ``social_core.backends.launchpad.LaunchpadOpenId``

`Ubuntu Launchpad <https://launchpad.net/>`_ OpenID doesn't require
major settings beside being defined on ``AUTHENTICATION_BACKENDS```::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.launchpad.LaunchpadOpenId',
        ...
    )
