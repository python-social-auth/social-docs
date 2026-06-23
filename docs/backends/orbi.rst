Orbi
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
   * - ``orbi``
     - ``social_core.backends.orbi.OrbiOAuth2``

Orbi OAuth v2 for Authentication.

- Register a new applicationat the `Orbi API`_, and

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_ORBI_KEY = ''
      SOCIAL_AUTH_ORBI_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_KAKAO_SCOPE = ['all']

.. _Orbi API: http://orbi.kr
