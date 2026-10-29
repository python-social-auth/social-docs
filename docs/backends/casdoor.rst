Casdoor
=======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``casdoor``
     - ``social_core.backends.casdoor.CasdoorOpenIdConnect``

The Casdoor_ backend authenticates against a self-hosted Casdoor server using
OpenID Connect.

In Casdoor, open your application and add your callback URL, typically
``https://your-domain.com/complete/casdoor/``, to **Redirect URLs**. Then copy
the application's **Client ID** and **Client secret** and configure::

    SOCIAL_AUTH_CASDOOR_OIDC_ENDPOINT = 'https://door.example.com'
    SOCIAL_AUTH_CASDOOR_KEY = '<client_id>'
    SOCIAL_AUTH_CASDOOR_SECRET = '<client_secret>'

The endpoint is the base URL of your Casdoor server. Do not append
``/.well-known/openid-configuration``. Trailing slashes are normalized. The
remaining configuration is auto-detected by fetching::

    <SOCIAL_AUTH_CASDOOR_OIDC_ENDPOINT>/.well-known/openid-configuration

The backend uses the authorization code flow with S256 PKCE enabled by
default, which Casdoor supports. You can turn it off if needed::

    SOCIAL_AUTH_CASDOOR_USE_PKCE = False

User details
------------

The Casdoor backend inherits defaults from ``open_id_connect.py``. Casdoor
returns the user's name in the ``preferred_username`` claim, which is used as
the username, and the display name in the ``name`` claim. Accounts are bound
to the stable ``sub`` claim, which is the Casdoor user ID. See the
`Casdoor OIDC client documentation`_ for the full list of claims.

The default scopes are ``openid``, ``profile`` and ``email``. You can request
additional scopes like this::

    SOCIAL_AUTH_CASDOOR_SCOPE = ['phone']

.. _Casdoor: https://casdoor.org/
.. _Casdoor OIDC client documentation: https://casdoor.org/docs/how-to-connect/oidc-client
