Pocket
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
   * - ``pocket``
     - ``social_core.backends.pocket.PocketAuth``

Pocket uses a weird variant of OAuth v2 that only defines a consumer key.

- Register a new application at the `Pocket API`_, and

- fill ``consumer key`` value in the settings::

      SOCIAL_AUTH_POCKET_KEY = ''

.. _Pocket API: http://getpocket.com/developer/
