MSN Live Connect
================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``live``
     - ``social_core.backends.live.LiveOAuth2``

Live uses OAuth2 for its connect workflow, notice that it isn't OAuth WRAP.

- Register a new application at `Live Connect Developer Center`_, set your site
  domain as redirect domain,

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_LIVE_KEY = ''
      SOCIAL_AUTH_LIVE_SECRET = ''

- Also it's possible to define extra permissions with::

     SOCIAL_AUTH_LIVE_SCOPE = [...]

  Defaults are ``wl.basic`` and ``wl.emails``. Latter one is necessary to
  retrieve user email.

- Ensure to have a valid ``Redirect URL`` (``http://your-domain/complete/live``)
  defined in the application if ``Enhanced security redirection`` is enabled.

.. _Live Connect Developer Center: https://account.live.com/developers/applications/create
