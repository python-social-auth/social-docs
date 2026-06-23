Withings
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
   * - ``withings``
     - ``social_core.backends.withings.WithingsOAuth``

Withings uses OAuth v1 for Authentication.

- Register a new application at the `Withings API`_, and

- fill ``Client ID`` and ``Client Secret`` from withings.com values in the settings::

      SOCIAL_AUTH_WITHINGS_KEY = ''
      SOCIAL_AUTH_WITHINGS_SECRET = ''

.. _Withings API: https://oauth.withings.com/partner/add
