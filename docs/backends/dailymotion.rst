DailyMotion
===========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``dailymotion``
     - ``social_core.backends.dailymotion.DailymotionOAuth2``

DailyMotion uses OAuth2. In order to enable the backend follow:

Accounts are associated by the stable provider ``id``. Associations created by
older social-core releases used the renameable screen name and migrate on the
next successful authentication.

- Register an application at `DailyMotion Developer Portal`_

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_DAILYMOTION_KEY = ''
    SOCIAL_AUTH_DAILYMOTION_SECRET = ''

- Set the ``Callback URL`` to ``http://<your hostname>/complete/dailymotion/``

- Specify scopes with::

    SOCIAL_AUTH_DAILYMOTION_SCOPE = [...]

  Available scopes are listed in the `Requesting Extended Permissions`_
  section.

.. _DailyMotion Developer Portal: http://www.dailymotion.com/profile/developer/new
.. _Requesting Extended Permissions: http://www.dailymotion.com/doc/api/authentication.html#requesting-extended-permissions
