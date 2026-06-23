Trello
======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``trello``
     - ``social_core.backends.trello.TrelloOAuth``

Trello provides OAuth1 support for their authentication process.

In order to enable it, follow:

- Generate an Application Key pair at `Trello Developers API Keys`_

- Fill **Consumer Key** and **Consumer Secret** settings::

    SOCIAL_AUTH_TRELLO_KEY = '...'
    SOCIAL_AUTH_TRELLO_SECRET = '...'

There are also two optional settings:

- your app name, otherwise the authorization page will say "Let An unknown application use your account?"::

    SOCIAL_AUTH_TRELLO_APP_NAME = 'My App'

- the expiration period, social auth defaults to 'never', but you can change it::

    SOCIAL_AUTH_TRELLO_EXPIRATION = '30days'


.. _Trello Developers API Keys: https://trello.com/1/appKey/generate
