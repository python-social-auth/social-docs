Auth0 OpenID Connect
=======================

Auth0 OpenID Connect (OIDC) implementation. Separate from
the previous ``Auth0OAuth2`` backend, as it builds on the base
OIDC backend.

To configure Auth0 as an OpenID Connect (OIDC) backend,
you need the following minimum configuration,
using details from your Auth0 tenant and an application
you have configured in it::

    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_DOMAIN = 'mytenant.auth0.com'
    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_KEY = '<client_id>'
    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_SECRET = '<client_secret>'

Scopes
-------

The default scope is ``["openid", "profile", "email"]``. In order to support
refresh tokens/long-lived logins, you may want to add the ``offline_access`` scope::

    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_SCOPE = 'openid profile email offline_access'
