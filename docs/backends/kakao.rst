Kakao
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
   * - ``kakao``
     - ``social_core.backends.kakao.KakaoOAuth2``

Kakao uses OAuth v2 for Authentication.

- Register a new applicationat the `Kakao API`_, and

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_KAKAO_KEY = ''
      SOCIAL_AUTH_KAKAO_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_KAKAO_SCOPE = [...]

.. _Kakao API: https://developers.kakao.com/docs/restapi
