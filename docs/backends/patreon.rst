Patreon
=======

Patreon supports OAuth 2.0

1. Register a new application at `Patreon Developer Portal`_.
2. Use the ``social.backends.patreon.PatreonOAuth2``, either by adding it to
   your ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS`` or instantiating it directly.
3. Fill in the the ``Client ID`` and ``Client Secret``::

    SOCIAL_AUTH_PATREON_KEY = '<your client ID>'
    SOCIAL_AUTH_PATREON_SECRET = '<your client secret>'

4. Checkout the `Patreon API Docs`_ for more information.

.. _Patreon Developer Portal: https://www.patreon.com/portal/registration/register-clients
.. _Patreon API Docs: https://docs.patreon.com/
