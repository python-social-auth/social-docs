Yahoo
=====

Yahoo supports OAuth2 for their auth flow.

OAuth 2.0 workflow, useful if you are planning to use Yahoo's API.

- Register a new application at `Yahoo Developer Center`_, set your app domain
  and configure scopes (they can't be overridden by application).

- Add the Yahoo OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.yahoo.YahooOAuth2',
        ...
    )

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_YAHOO_OAUTH2_KEY = ''
      SOCIAL_AUTH_YAHOO_OAUTH2_SECRET = ''


.. _Yahoo Developer Center: https://developer.yahoo.com/
