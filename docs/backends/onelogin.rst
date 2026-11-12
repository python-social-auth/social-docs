OneLogin
========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``onelogin``
     - ``social_core.backends.onelogin.OneLoginOpenIdConnect``

The OneLogin_ backend uses OpenID Connect authorization code flow with S256
PKCE enabled by default.

Configuration
-------------

Create an OpenID Connect application in OneLogin and enable the authorization
code grant. Register your application's callback URL, typically
``https://your-domain.com/complete/onelogin/``, in **Redirect URIs**.
On the **SSO** tab, set the **Token Endpoint Authentication Method** to
**POST**. Copy the **Client ID**, **Client Secret**, and **Issuer URL** and
configure::

    SOCIAL_AUTH_ONELOGIN_OIDC_ENDPOINT = 'https://example.onelogin.com/oidc/2'
    SOCIAL_AUTH_ONELOGIN_KEY = '<client_id>'
    SOCIAL_AUTH_ONELOGIN_SECRET = '<client_secret>'

Use your tenant's issuer URL as the endpoint, without
``/.well-known/openid-configuration``. Trailing slashes are normalized. The
backend discovers the authorization, token, user-info, signing-key, and issuer
configuration from::

    <SOCIAL_AUTH_ONELOGIN_OIDC_ENDPOINT>/.well-known/openid-configuration

Client credentials are sent in the token request body using
``client_secret_post``. This matches OneLogin's **POST** authentication method.
The token request uses HTTP POST; the authentication method controls where
credentials are sent, rather than changing the HTTP method.

PKCE
----

OneLogin advertises support for S256 in its `provider configuration`_. The
backend sends an S256 challenge in the authorization request and the matching
verifier when exchanging the authorization code. Client-secret authentication
is retained; configure the OneLogin application for **POST**, rather than the
separate **None (PKCE)** mode for public clients.

For a deployment that requires disabling PKCE, configure::

    SOCIAL_AUTH_ONELOGIN_USE_PKCE = False

Disabling PKCE removes the verifier binding between the authorization request
and token exchange. Keep it enabled when supported by your application.

User details
------------

The default scopes are ``openid``, ``profile`` and ``email``. Accounts are bound
to the stable ``sub`` claim. Profile fields use the shared :doc:`oidc` defaults,
including ``preferred_username``, ``name``, ``given_name``, ``family_name`` and
``email``. Additional scopes can be requested with::

    SOCIAL_AUTH_ONELOGIN_SCOPE = ['groups']

For group extraction and restrictions, see :doc:`/groups`.

Existing integrations
---------------------

This backend uses the name ``onelogin`` for callbacks, settings, and stored
account associations. An existing integration using the generic ``oidc``
backend or a custom subclass has a different backend namespace. Switching
classes does not migrate existing associations. Plan and validate an explicit
association migration, including conflicts, before switching an existing
deployment; do not automatically relink accounts by email.

.. _OneLogin: https://www.onelogin.com/
.. _provider configuration: https://developers.onelogin.com/docs/openid-connect/api/provider-config/
