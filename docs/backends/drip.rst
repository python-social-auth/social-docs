Drip
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
   * - ``drip``
     - ``social_core.backends.drip.DripOAuth``

Drip uses OAuth v2 for Authentication.

- Register a new application with `Drip`_, and

- fill ``Client ID`` and ``Client Secret`` from getdrip.com values in
  the settings::

      SOCIAL_AUTH_DRIP_KEY = ''
      SOCIAL_AUTH_DRIP_SECRET = ''

.. _Drip: https://www.getdrip.com/user/applications
