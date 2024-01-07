Etsy OAuth2
=============================

Etsy supports the `OAuth 2.0`_ protocol using Authorization code with `Proof Key for Code Exchange (PKCE)`_ flow.

Configuration
--------------

1. Register a new `Application Link`_ in your Etsy Account.

2. Fill *Client ID* in ``SOCIAL_AUTH_ETSY_OAUTH2_KEY`` in your project settings::

    SOCIAL_AUTH_ETSY_OAUTH2_KEY = "..."

   Note: *Client Secret* isn't required via this flow.

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        "social_core.backends.etsy.EtsyOAuth2",
        ...
    )

Extra Configuration
--------------------

- You can specify the scope that your application requires::

    SOCIAL_AUTH_ETSY_OAUTH2_SCOPE = ["shops_r", "shops_w", ...]

  You can see all possible values at `Etsy OAuth 2.0 provider API Scopes`_.

- You can specify PKCE challenge method::

    SOCIAL_AUTH_ETSY_OAUTH2_PKCE_CODE_CHALLENGE_METHOD = '...'

  The possible value for this is only ``S256`` which is set by default.

  You can see more information about PKCE at `RFC7636`_.

.. _OAuth 2.0: https://developer.etsy.com/documentation/essentials/authentication
.. _Application Link: https://developer.etsy.com/documentation/#developing-a-new-open-api-app
.. _Proof Key for Code Exchange (PKCE): https://datatracker.ietf.org/doc/html/rfc7636
.. _RFC7636: https://datatracker.ietf.org/doc/html/rfc7636
.. _Etsy OAuth 2.0 provider API Scopes: https://developer.etsy.com/documentation/essentials/authentication/#scopes