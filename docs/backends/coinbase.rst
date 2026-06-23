Coinbase
========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``coinbase``
     - ``social_core.backends.coinbase.CoinbaseOAuth2``

Coinbase uses OAuth2.

- Register an application at Coinbase_

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_COINBASE_KEY = ''
    SOCIAL_AUTH_COINBASE_SECRET = ''

- Set the ``redirect_url`` on coinbase. Make sure to include the trailing
  slash, eg. ``http://hostname/complete/coinbase/``

- Specify scopes with::

    SOCIAL_AUTH_COINBASE_SCOPE = [...]

  By default the scope is set to ``balance``.

- extra scopes can be defined by using::

    SOCIAL_AUTH_COINBASE_AUTH_EXTRA_ARGUMENTS = {'account': 'all'}

.. _Coinbase: https://coinbase.com/oauth/applications/new
