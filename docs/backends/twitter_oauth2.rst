Twitter API v2
==============

Twitter offers per application keys named ``Client ID`` and ``Client Secret``.
To enable Twitter these two keys are needed. Further documentation at
`Twitter development resources`_:

- Register a new application at `Twitter App Creation`_,

- Fill **Client ID** and **Client Secret** values::

      SOCIAL_AUTH_TWITTER_OAUTH2_KEY = ''
      SOCIAL_AUTH_TWITTER_OAUTH2_SECRET = ''

- You can specify PKCE challenge method following::  

      SOCIAL_AUTH_TWITTER_OAUTH2_PKCE_CODE_CHALLENGE_METHOD = ''

  The possible values for configuration are ``s256`` and ``plain``.
  By default, ``s256`` is set.

  You can see more information about PKCE at `RFC7636`_. 

- You need to specify an URL callback or the OAuth will raise a "403 Client Error".
  The callback URL should be something like "https://example.com/complete/twitter-oauth2"


.. _Twitter development resources: https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
.. _Twitter App Creation: https://developer.twitter.com/en/portal/dashboard
.. _RFC7636: https://datatracker.ietf.org/doc/html/rfc7636
