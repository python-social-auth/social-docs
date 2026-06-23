RunKeeper
=========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``runkeeper``
     - ``social_core.backends.runkeeper.RunKeeperOAuth2``

RunKeeper uses OAuth v2 for authentication.

- Register a new application at the `RunKeeper API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_RUNKEEPER_KEY = ''
      SOCIAL_AUTH_RUNKEEPER_SECRET = ''

.. _RunKeeper API: http://developer.runkeeper.com/healthgraph
