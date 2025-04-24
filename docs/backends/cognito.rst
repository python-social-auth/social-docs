Cognito
=======

Cognito implemented OAuth2 protocol for their authentication mechanism. To
enable ``python-social-auth`` support follow this steps:

1. Go to `AWS Cognito Console`_ and select ``Manage User Pools``.

2. Choose an existing pool or create a new one following the `Cognito Pool
   Tutorial`_.

3. Create an app (make sure to generate a client secret) and configure a pool
   domain (`Cognito App Configuration`_)::

    SOCIAL_AUTH_COGNITO_KEY = '...'
    SOCIAL_AUTH_COGNITO_SECRET = '...'
    SOCIAL_AUTH_COGNITO_POOL_DOMAIN = '...'

4. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.cognito.CognitoOAuth2',
        ...
    )

.. _AWS Cognito Console: https://console.aws.amazon.com/cognito/home
.. _Cognito Pool Tutorial: https://docs.aws.amazon.com/cognito/latest/developerguide/tutorial-create-user-pool.html
.. _Cognito App Configuration: Getting Started for Web: https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-user-pools-configuring-app-integration.html
