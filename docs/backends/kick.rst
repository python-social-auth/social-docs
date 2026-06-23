Kick
====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``kick``
     - ``social_core.backends.kick.KickOAuth2``

Kick works similar to Facebook (OAuth) but with Oauth2.1.

- Register a new application in the `developer tab`_ of your Kick settings
  page, set the callback URL to ``http://example.com/complete/kick/``
  replacing ``example.com`` with your domain.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_KICK_KEY = ''
      SOCIAL_AUTH_KICK_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_KICK_SCOPE = [...]

Further documentation at `Developer Guide`_.

.. _developer tab: https://kick.com/settings/developer
.. _Developer Guide: https://docs.kick.com/getting-started/generating-tokens-oauth2-flow
