XING
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
   * - ``xing``
     - ``social_core.backends.xing.XingOAuth``

XING uses OAuth1 for their auth mechanism, in order to enable the backend
follow:

- Register a new application at `XING Apps Dashboard`_,

- Fill **Consumer Key** and **Consumer Secret** values::

      SOCIAL_AUTH_XING_KEY = ''
      SOCIAL_AUTH_XING_SECRET = ''

.. _XING Apps Dashboard: https://dev.xing.com/applications
