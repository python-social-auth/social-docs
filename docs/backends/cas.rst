CAS (OpenID Connect via Apereo CAS)
=====================

The CAS_ backend allows authentication against an Apereo CAS OIDC provider.
The backend class is `CASOpenIdConnectAuth` with name `cas`.  A minimum
configuration is::

    SOCIAL_AUTH_CAS_OIDC_ENDPOINT = 'https://.....'
    SOCIAL_AUTH_CAS_KEY = '<client_id>'
    SOCIAL_AUTH_CAS_SECRET = '<client_secret>'

The remaining configuration will be auto-detected, by fetching::

    <SOCIAL_AUTH_CAS_OIDC_ENDPOINT>/.well-known/openid-configuration

This class functions identically to the generic OIDC backend, but hides
the differences in implementation details of the OIDC implementation in
Apereo CAS.

Note that dispite the naming of the backend, this is NOT an implementation
of the CAS protocol, also supported by Apereo CAS. The CAS backend is only
intended as a way to use the Apereo CAS identity provider as an
authentication service, but via OIDC.

Username
--------

The CAS_ backend will check for a ``preferred_username`` key in the values
returned by the server.  If the username is under a different key, this can
be overridden::

    SOCIAL_AUTH_CAS_USERNAME_KEY = 'nickname'

This setting indicates that the username should be populated by the
``nickname`` claim instead.

Scopes
------

The default set of scopes requested are "openid", "profile" and "email".
You can request additional claims, for example::

    SOCIAL_AUTH_CAS_SCOPE = ['groups']

and you can prevent the inclusion of the default scopes using::

    SOCIAL_AUTH_CAS_IGNORE_DEFAULT_SCOPE = True

.. _CAS: https://apereo.github.io/cas/6.6.x/authentication/OIDC-Authentication.html
