Just Giving
===========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``justgiving``
     - ``social_core.backends.justgiving.JustGivingOAuth2``

OAuth2
------

Follow the steps at `Just Giving API Docs`_ to register your
application and get the needed keys.

- Add the Just Giving OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.justgiving.JustGivingOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_JUSTGIVING_KEY = ''
      SOCIAL_AUTH_JUSTGIVING_SECRET = ''

.. _Just Giving API Docs: https://api.justgiving.com/docs
