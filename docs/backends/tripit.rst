TripIt
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
   * - ``tripit``
     - ``social_core.backends.tripit.TripItOAuth``

TripIt offers per application keys named ``API Key`` and ``API Secret``.
To enable TripIt these two keys are needed. Further documentation at
`TripIt Developer Center`_:

- Register a new application at `TripIt App Registration`_,

- fill **API Key** and **API Secret** values::

    SOCIAL_AUTH_TRIPIT_KEY = ''
    SOCIAL_AUTH_TRIPIT_SECRET = ''

.. _TripIt Developer Center: https://www.tripit.com/developer
.. _TripIt App Registration: https://www.tripit.com/developer/create
