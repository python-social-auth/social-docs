Steam OpenID
============

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``steam``
     - ``social_core.backends.steam.SteamOpenId``

Steam OpenID works quite straightforward, but to retrieve some user data (known
as ``player`` on Steam API) a Steam API Key is needed.

Configurable settings:


1. Supply a Steam API Key from `Steam Dev`_

2. Fill key in your project settings::

    SOCIAL_AUTH_STEAM_API_KEY = '...'

3. To save ``player`` data provided by Steam into ``extra_data``::

	SOCIAL_AUTH_STEAM_EXTRA_DATA = ['player']

4. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.steam.SteamOpenId',
        ...
    )

.. _Steam Dev: http://steamcommunity.com/dev/apikey
