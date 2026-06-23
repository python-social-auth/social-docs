Twilio
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
   * - ``twilio``
     - ``social_core.backends.twilio.TwilioAuth``

- Register a new application at `Twilio Connect Api`_

- Fill ``SOCIAL_AUTH_TWILIO_KEY`` and ``SOCIAL_AUTH_TWILIO_SECRET`` values in
  the settings::

    SOCIAL_AUTH_TWILIO_KEY = ''
    SOCIAL_AUTH_TWILIO_SECRET = ''

- Add desired authentication backends to Django's ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``
  setting::

    'social_core.backends.twilio.TwilioAuth',

- Usage example::

    <a href="/login/twilio">Enter using Twilio</a>


.. _Twilio Connect API: https://www.twilio.com/user/account/connect/apps
