Sketchfab
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
   * - ``sketchfab``
     - ``social_core.backends.sketchfab.SketchfabOAuth2``

Sketchfab uses OAuth 2 for authentication.

To use:

- Follow the steps at `Sketchfab Oauth`_, and ask for an
  ``Authorization code`` grant type.

- Fill the ``Client id/key`` and ``Client Secret`` values you received
  in your django settings::

      SOCIAL_AUTH_SKETCHFAB_KEY   = ''
      SOCIAL_AUTH_SKETCHFAB_SECRET = ''

.. _Sketchfab Oauth: https://sketchfab.com/developers/oauth
