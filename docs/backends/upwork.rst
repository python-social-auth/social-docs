Upwork
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
   * - ``upwork``
     - ``social_core.backends.upwork.UpworkOAuth``

Upwork supports only OAuth 1.

- Register a new application at `Upwork Developers`_.

OAuth1
------

Add the Upwork OAuth backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.upwork.UpworkOAuth',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_UPWORK_KEY = ''
      SOCIAL_AUTH_UPWORK_SECRET = ''


**Note:** For more information please go to `Upwork API Reference`_.

.. _Upwork Developers: https://www.upwork.com/services/api/apply
.. _Upwork API Reference: https://developers.upwork.com/?lang=python
