SimpleLogin
===========

SimpleLogin uses OAuth 2.0 for Authentication.

- On your project settings, you should add SimpleLogin on your
  ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.simplelogin.SimpleLoginOAuth2',
    )

- Register a new app at `SimpleLogin App`_. By default, SimpleLogin whitelists
  ``localhost`` so your app should work locally.
  Please set the callback URL to ``http://example.com/complete/simplelogin/``
  replacing ``example.com`` with your domain when you deploy your web app to
  production.

- Add these values of ``Client ID`` and ``Client Secret`` from SimpleLogin in
  your project settings file.

The ``Client ID`` should be added on ``SOCIAL_AUTH_SIMPLELOGIN_KEY`` and the
``Client Secret`` should be added on ``SOCIAL_AUTH_SIMPLELOGIN_SECRET``::

      SOCIAL_AUTH_SIMPLELOGIN_KEY = 'client-id'
      SOCIAL_AUTH_SIMPLELOGIN_SECRET = 'very-secret'

.. _SimpleLogin App: https://app.simplelogin.io
