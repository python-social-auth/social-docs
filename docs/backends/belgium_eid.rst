Belgium EID
===========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``belgiumeid``
     - ``social_core.backends.belgiumeid.BelgiumEIDOpenId``

Belgium EID OpenID doesn't require major settings beside being defined on
``AUTHENTICATION_BACKENDS```::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.belgiumeid.BelgiumEIDOpenId',
        ...
    )
