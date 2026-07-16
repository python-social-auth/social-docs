Helmholtz AAI (OpenID Connect)
==============================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``helmholtz``
     - ``social_core.backends.helmholtz.HelmholtzOpenIdConnect``

The Helmholtz backend allows authentication against the `Helmholtz AAI`_,
the authentication and authorization infrastructure of the Helmholtz
Association operated by HIFIS_.

To obtain a client id and secret, and for the requested scopes to be
released, you have to register your service with the OP. See the
`Helmholtz AAI documentation`_ for details.

A minimum configuration is::

    SOCIAL_AUTH_HELMHOLTZ_KEY = '<client_id>'
    SOCIAL_AUTH_HELMHOLTZ_SECRET = '<client_secret>'

The remaining configuration is auto-detected by fetching::

    https://login.helmholtz.de/oauth2/.well-known/openid-configuration

Username
--------

The backend reads the username from the ``preferred_username`` claim
returned by the server. If the username is under a different key, this can
be overridden::

    SOCIAL_AUTH_HELMHOLTZ_USERNAME_KEY = 'nickname'

This setting indicates that the username should be populated from the
``nickname`` claim instead.

Scopes
------

By default the backend requests, besides ``openid``, ``profile`` and
``email``, the scopes ``voperson_id``, ``eduperson_entitlement``,
``eduperson_scoped_affiliation``, ``voperson_external_affiliation``,
``eduperson_assurance`` and ``orcid``. You can request additional scopes,
for example::

    SOCIAL_AUTH_HELMHOLTZ_SCOPE = ['display_name']

Restricting access by entitlement
---------------------------------

Access to the service can be restricted to users holding certain
entitlements (typically representing membership in a virtual
organization)::

    SOCIAL_AUTH_HELMHOLTZ_ALLOWED_ENTITLEMENTS = [
        'urn:geant:helmholtz.de:group:my-vo#login.helmholtz.de',
    ]

A user holding any of the listed entitlements is allowed to log in. If the
list is empty (the default), all users are allowed.

The entitlements are read from the ``eduperson_entitlement`` claim. If your
deployment provides them under a different claim, this can be overridden::

    SOCIAL_AUTH_HELMHOLTZ_ENTITLEMENT_KEY = 'entitlement'

.. _Helmholtz AAI: https://hifis.net/aai/
.. _HIFIS: https://hifis.net
.. _Helmholtz AAI documentation: https://hifis.net/doc/helmholtz-aai/
