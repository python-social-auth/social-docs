Auth0 OpenID Connect
=======================

Auth0 OpenID Connect (OIDC) implementation. Separate from
the previous ``Auth0OAuth2`` backend, as it builds on the base
OIDC backend.

IdP Setup
---------

To configure Auth0:

1. Log into your Auth0 Dashboard
2. Navigate to **Applications** > **Create Application**
3. Select **Regular Web Applications**
4. In the application settings, configure:

   * **Allowed Callback URLs**: ``https://your-domain.com/complete/auth0-openidconnect/``
   * **Allowed Logout URLs**: ``https://your-domain.com/logout/`` (if using logout)
   * **Allowed Web Origins**: ``https://your-domain.com``

5. Note the **Domain** (e.g., ``mytenant.auth0.com``), **Client ID**, and **Client Secret**

Application Configuration
-------------------------

Use the values from your Auth0 application::

    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_DOMAIN = 'mytenant.auth0.com'
    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_KEY = '<client_id>'
    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_SECRET = '<client_secret>'

Scopes
-------

The default scope is ``["openid", "profile", "email"]``. In order to support
refresh tokens/long-lived logins, you may want to add the ``offline_access`` scope::

    SOCIAL_AUTH_AUTH0_OPENIDCONNECT_SCOPE = 'openid profile email offline_access'
