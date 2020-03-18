AppleID
=======

Apple ID implemented OAuth2 and OpenID Connect protocols for their authentication mechanism. To
enable ``python-social-auth`` support follow this steps:

1. Go to `Apple Developer Portal`_ and

  1. `Create or select an existing App ID`_
  2. `Create a Sign Certificate`_
  3. `Create a Services ID`_, activate "Sign In with Apple" and grant your "return URLs"

2. Fill App Id and Secret in your project settings::

    SOCIAL_AUTH_APPLE_ID_CLIENT = '...'             # Your client_id com.application.your, aka "Service ID"
    SOCIAL_AUTH_APPLE_ID_TEAM = '...'               # Your Team ID, ie K2232113
    SOCIAL_AUTH_APPLE_ID_KEY = '...'                # Your Key ID, ie Y2P99J3N81K
    SOCIAL_AUTH_APPLE_ID_SECRET = """
    -----BEGIN PRIVATE KEY-----
    MIGTAgE.....
    -----END PRIVATE KEY-----"""
    SOCIAL_AUTH_APPLE_ID_SCOPE = ['email', 'name']
    SOCIAL_AUTH_APPLE_ID_EMAIL_AS_USERNAME = True   # If you want to use email as username

3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.apple.AppleIdAuth',
        ...
    )

Further documentation at `Website Developer Guide`_ and `Getting Started`_.

.. _Apple Developer Portal: https://developer.apple.com/
.. _Website Developer Guide: https://developer.apple.com/documentation/signinwithapplerestapi/authenticating_users_with_sign_in_with_apple
.. _Getting Started: https://developer.apple.com/sign-in-with-apple/get-started/
.. _Authenticating users: https://developer.apple.com/documentation/signinwithapplerestapi/authenticating_users_with_sign_in_with_apple
.. _Create a Sign Certificate: https://help.apple.com/developer-account/?lang=en#/dev77c875b7e
.. _Create or select an existing App ID: https://help.apple.com/developer-account/?lang=en#/devde676e696
.. _Create a Services ID: https://help.apple.com/developer-account/?lang=en#/dev1c0e25352
