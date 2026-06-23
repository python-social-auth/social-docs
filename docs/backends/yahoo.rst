Yahoo
=====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``yahoo-oauth2``
     - ``social_core.backends.yahoo.YahooOAuth2``

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
