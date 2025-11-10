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

IdP Setup
---------

To configure your OIDC Identity Provider for use with this backend:

1. Create a new application/client in your IdP with type "Web Application"
2. Set the **Redirect URI** (also called Callback URL) to::

    https://your-domain.com/complete/oidc/

   Replace ``your-domain.com`` with your actual application domain.

3. Configure scopes to include at minimum: ``openid``, ``profile``, ``email``
4. Note the generated **Client ID** and **Client Secret** for use in your Django settings above
5. Ensure your IdP exposes the OpenID Connect discovery endpoint at: ``https://your-idp-domain/.well-known/openid-configuration``

.. note::
   For development, you can use ``http://localhost:8000/complete/oidc/`` as the redirect URI.

Authentication Request Parameters
---------------------------------

All this parameters are optional and they might not be supported by the OIDC provider.

Prompt
^^^^^^

This informs the OIDC provider whether the OIDC provider prompts the user for reauthentication and consent. ::

    SOCIAL_AUTH_OIDC_PROMPT = '<prompt> ...'

Defined values are

- ``none``
- ``login``
- ``consent``
- ``select_account``

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
