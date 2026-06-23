MapMyFitness
============

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``mapmyfitness``
     - ``social_core.backends.mapmyfitness.MapMyFitnessOAuth2``

MapMyFitness uses OAuth v2 for authentication.

- Register a new application at the `MapMyFitness API`_, and

- fill ``key`` and ``secret`` values in the settings::

      SOCIAL_AUTH_MAPMYFITNESS_KEY = ''
      SOCIAL_AUTH_MAPMYFITNESS_SECRET = ''

.. _MapMyFitness API: https://www.mapmyapi.com
