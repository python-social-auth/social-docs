OpenStreetMap OAuth 2
=====================

OpenStreetMap supports the OAuth 2.0 protocol. It supports two types of OAuth 2.0 flows:

1. Authorization code with `Proof Key for Code Exchange (PKCE)`_
2. Authorization code

Configuration
-------------

- Login to your account

- Register your application as OAuth 2 application on the `My Client Applications page`_

  * Set the redirect URIs to https://example.com/complete/openstreetmap-oauth2/
  * PKCE can be enabled/disabled using the "Confidential application?" flag.
  * Select all required Permissions.
  * Scopes names are shown next to each permission after saving.

- Fill *Client ID* in ``SOCIAL_AUTH_OPENSTREETMAP_OAUTH2_KEY`` and
  *Client Secret* in ``SOCIAL_AUTH_OPENSTREETMAP_OAUTH2_SECRET``

      SOCIAL_AUTH_OPENSTREETMAP_OAUTH2_KEY = '...'
      SOCIAL_AUTH_OPENSTREETMAP_OAUTH2_SECRET = '...'

  Note: *Client Secret* isn't required for PKCE.

- Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
      ...
     'social_core.backends.openstreetmap_oauth2.OpenStreetMapOAuth2',
     ...
    )

Access tokens currently do not expire automatically.

More documentation at `OpenStreetMap Wiki`_:

Extra Configuration
--------------------

- You can specify the scopes that your application requires::

    SOCIAL_AUTH_OPENSTREETMAP_OAUTH2_SCOPE  = [ 'read_prefs' ]

- You can choose to disable PKCE::

    SOCIAL_AUTH_OPENSTREETMAP_OAUTH2_USE_PKCE = False

  By default, `True` is set.


.. _OpenStreetMap Wiki: http://wiki.openstreetmap.org/wiki/OAuth
.. _My Client Applications page: https://www.openstreetmap.org/oauth2/applications
.. _Proof Key for Code Exchange (PKCE): https://datatracker.ietf.org/doc/html/rfc7636
