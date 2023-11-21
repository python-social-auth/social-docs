Bitbucket Data Center OAuth2
=============================

Bitbucket Data Center (previously Bitbucket Server) supports the `OAuth 2.0`_ protocol. It supports two types of OAuth 2.0 flows:

1. Authorization code with `Proof Key for Code Exchange (PKCE)`_
2. Authorization code

Configuration
--------------

1. Register a new `Application Link`_ in your Bitbucket Data Center instance.

2. Provide the host URL of your Bitbucket Data Center instance::

    SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_URL = "https://my-bitbucket-server.acme.com"

3. Fill *Client ID* in ``SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_KEY`` and *Client Secret* in ``SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_SECRET`` in your project settings::

    SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_KEY = "..."
    SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_SECRET = "..."

4. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        "social_core.backends.bitbucket_datacenter.BitbucketDataCenterOAuth2",
        ...
    )

Extra Configuration
--------------------

- You can specify the scope that your application requires::

    SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_SCOPE = ["PUBLIC_REPOS"]

  You can see all possible values at `Bitbucket Data Center OAuth 2.0 provider API`_. By default, ``PUBLIC_REPOS`` is set.

- You can choose to disable PKCE::

    SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_USE_PKCE = False

  By default, `True` is set.

- You can specify PKCE challenge method::

    SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_PKCE_CODE_CHALLENGE_METHOD = '...'

  The possible values for this are ``s256`` and ``plain``.
  By default, ``s256`` is set.

  You can see more information about PKCE at `RFC7636`_. 

- You can specify the user's avatar size::

    SOCIAL_AUTH_BITBUCKET_DATACENTER_OAUTH2_USER_AVATAR_SIZE = 48

  This is the size of the user's avatar requested from the API which is stored in ``EXTRA_DATA["avatar_url"]``. By default, ``48`` is set.

.. _OAuth 2.0: https://confluence.atlassian.com/bitbucketserver/bitbucket-oauth-2-0-provider-api-1108483661.html
.. _Application Link: https://confluence.atlassian.com/bitbucketserver/configure-an-incoming-link-1108483657.html
.. _Proof Key for Code Exchange (PKCE): https://datatracker.ietf.org/doc/html/rfc7636
.. _RFC7636: https://datatracker.ietf.org/doc/html/rfc7636
.. _Bitbucket Data Center OAuth 2.0 provider API: https://confluence.atlassian.com/bitbucketserver/bitbucket-oauth-2-0-provider-api-1108483661.html#BitbucketOAuth2.0providerAPI-scopes