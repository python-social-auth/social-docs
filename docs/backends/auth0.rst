Auth0
=====

Auth0 OAuth2
------------

Auth0 provides OAuth2 authentication. This is the original ``Auth0OAuth2`` backend.

For a newer OpenID Connect implementation, see :doc:`auth0_openidconnect`.

Setup
*****

To enable Auth0 OAuth2 support:

1. Register your application at `Auth0 Dashboard`_ to get your Auth0 domain,
   Client ID, and Client Secret.

2. Fill in the settings with your Auth0 domain, Client ID, and Client Secret::

    SOCIAL_AUTH_AUTH0_KEY = ''
    SOCIAL_AUTH_AUTH0_SECRET = ''
    SOCIAL_AUTH_AUTH0_DOMAIN = 'yourdomain.auth0.com'

   Replace ``yourdomain`` with your Auth0 tenant domain.

3. Add the backend to your authentication backends::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.auth0.Auth0OAuth2',
        ...
    )

Scopes
******

You can define custom scopes using the ``SOCIAL_AUTH_AUTH0_SCOPE`` setting::

    SOCIAL_AUTH_AUTH0_SCOPE = ['openid', 'profile', 'email']

The backend will handle JWT token validation and extract user details including
username, email, full name, and profile picture.

.. _Auth0 Dashboard: https://manage.auth0.com/
