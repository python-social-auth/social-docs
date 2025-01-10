Yahoo
=====

Yahoo supports OpenID and OAuth2 for their auth flow.


Yahoo OpenID
------------

OpenID doesn't require any particular configuration beside enabling the backend
in the ``AUTHENTICATION_BACKENDS`` setting::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.yahoo.YahooOAuth2',
        ...
    )


Yahoo OAuth2
------------
OAuth 2.0 workflow, useful if you are planning to use Yahoo's API.

- Register a new application at `Yahoo Developer Center`_, set your app domain
  and configure scopes (they can't be overridden by application).

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_YAHOO_OAUTH2_KEY = ''
      SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = ''


.. _Yahoo Developer Center: https://developer.yahoo.com/
