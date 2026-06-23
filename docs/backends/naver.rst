Naver
=====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``naver``
     - ``social_core.backends.naver.NaverOAuth2``

Naver uses OAuth v2 for Authentication.

- Register a new application at the `Naver API`_, and

- add naver oauth backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.naver.NaverOAuth2',
        ...
    )

- fill ``Client ID`` and ``Client Secret`` from developer.naver.com
  values in the settings::

	SOCIAL_AUTH_NAVER_KEY = ''
	SOCIAL_AUTH_NAVER_SECRET = ''

- you can get EXTRA_DATA::

	SOCIAL_AUTH_NAVER_EXTRA_DATA = ['nickname', 'gender', 'age',
                                        'birthday', 'profile_image']

.. _Naver API: https://nid.naver.com/devcenter/docs.nhn?menu=API
