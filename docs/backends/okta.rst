Okta
====

This section describes how to setup the different services provided by Okta.

Okta OAuth2
-----------

To enable OAuth2 support:

- Fill ``Client ID``, ``Client Secret`` and `API URL (e.g.
  https://dev-000000.oktapreview.com/oauth2)` settings, these values can be
  obtained easily from Okta after creating a Web application. Please note, do
  not use the ``/oauth2/default`` endpoint for Okta authentication::

      SOCIAL_AUTH_OKTA_OAUTH2_KEY = ''
      SOCIAL_AUTH_OKTA_OAUTH2_SECRET = ''
      SOCIAL_AUTH_OKTA_OAUTH2_API_URL = ''

Okta OpenId Connect
-------------------

- Fill ``Client ID``, ``Client Secret`` and `API URL (e.g.
  https://dev-000000.oktapreview.com/oauth2)` settings, these values can be
  obtained easily from Okta after creating a Web application. Please note, do
  not use the ``/oauth2/default`` endpoint for Okta authentication::

      SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY = ''
      SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET = ''
      SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL = ''
