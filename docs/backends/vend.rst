Vend
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
   * - ``vend``
     - ``social_core.backends.vend.VendOAuth2``

Vend supports OAuth 2.

- Register a new application at `Vend Developers Portal`_

- Add the Vend OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.vend.VendOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_VEND_OAUTH2_KEY = ''
      SOCIAL_AUTH_VEND_OAUTH2_SECRET = ''

More details on their docs_.

.. _Vend Developers Portal: https://developers.vendhq.com/developer/applications
.. _docs: https://developers.vendhq.com/documentation
