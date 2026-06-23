Twitch
======

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``twitch``
     - ``social_core.backends.twitch.TwitchOpenIdConnect``
   * - ``twitch``
     - ``social_core.backends.twitch.TwitchOAuth2``

Twitch works similar to Facebook (OAuth).

- Register a new application in the `connections tab`_ of your Twitch settings
  page, set the callback URL to ``http://example.com/complete/twitch/``
  replacing ``example.com`` with your domain.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_TWITCH_KEY = ''
      SOCIAL_AUTH_TWITCH_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_TWITCH_SCOPE = [...]

.. _connections tab: http://www.twitch.tv/settings/connections
