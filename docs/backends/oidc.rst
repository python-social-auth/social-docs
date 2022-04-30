OIDC (OpenID Connect)
=====================

The OIDC_ backend allows authentication against a generic OIDC provider.
The backend class is `OpenIdConnectAuth` with name `oidc`.  A minimum
configuration is::

    SOCIAL_AUTH_OIDC_OIDC_ENDPOINT = 'https://.....'
    SOCIAL_AUTH_OIDC_KEY = '<client_id>'
    SOCIAL_AUTH_OIDC_SECRET = '<client_secret>'

The remaining configuration will be auto-detected, by fetching::

    <SOCIAL_AUTH_OIDC_OIDC_ENDPOINT>/.well-known/openid-configuration

This class can be used standalone, but is also the base class for some other
backends.

Username
--------

The OIDC_ backend will check for a ``preferred_username`` key in the values
returned by the server.  If the username is under a different key, this can
be overridden::

    SOCIAL_AUTH_OIDC_USERNAME_KEY = 'nickname'

This setting indicates that the username should be populated by the
``nickname`` claim instead.

Scopes
------

The default set of scopes requested are "openid", "profile" and "email".
You can request additional claims, for example::

    SOCIAL_AUTH_OIDC_SCOPE = ['groups']

and you can prevent the inclusion of the default scopes using::

    SOCIAL_AUTH_OIDC_IGNORE_DEFAULT_SCOPE = True

.. _OIDC: https://openid.net/connect/
