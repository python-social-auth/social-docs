Discord
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
   * - ``discord``
     - ``social_core.backends.discord.DiscordOAuth2``

Discord uses OAuth2 for authentication.

- Register a new application at the `Discord Developer Portal`_, set the
  callback URL to ``http://example.com/complete/discord/`` replacing
  ``example.com`` with your domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_DISCORD_KEY = ''
      SOCIAL_AUTH_DISCORD_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_DISCORD_SCOPE = [...]

  See available scopes at `Discord OAuth2 Scopes`_.

.. _Discord Developer Portal: https://discord.com/developers/applications
.. _Discord OAuth2 Scopes: https://discord.com/developers/docs/topics/oauth2#shared-resources-oauth2-scopes
