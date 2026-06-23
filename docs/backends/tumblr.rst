Tumblr
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
   * - ``tumblr``
     - ``social_core.backends.tumblr.TumblrOAuth``

Tumblr uses OAuth 1.0a for authentication.

- Register a new application at http://www.tumblr.com/oauth/apps

- Set the ``Default callback URL`` to http://[your domain]/

- fill ``OAuth Consumer Key`` and ``Secret Key`` values in your Django
  settings::

      SOCIAL_AUTH_TUMBLR_KEY = ''
      SOCIAL_AUTH_TUMBLR_SECRET = ''

.. _Tumblr API: http://www.tumblr.com/docs/en/api/v2
