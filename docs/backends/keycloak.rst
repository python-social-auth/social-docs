Keycloak - Open Source Red Hat SSO
==================================

Keycloak is an open source IAM and SSO system.

To enable Keycloak as a backend:

- On your project settings, add Keycloak on your ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.keycloak.KeycloakOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    )

- Create a Client in your Keycloak realm

- On your client under ``Fine Grain OpenID Connect Configuration`` ensure that ``User Info Signed Response Algorithm`` and ``Request Object Signature Algorithm`` is set to ``RS256``. Save. Then go to: Realm Settings -> Keys -> RS256 and copy your Public key to ``SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY`` in your django settings

- Add these values of ``Client ID`` and ``Client Secret`` from client in your project settings file.

The ``Client ID`` should be added on ``SOCIAL_AUTH_KEYCLOAK_KEY`` and the ``Client Secret`` should be
added on ``SOCIAL_AUTH_KEYCLOAK_SECRET``. You also need to add your keycloak instance auth and token URL's found in the Realm OpenID Endpoint Configuration::

    SOCIAL_AUTH_KEYCLOAK_KEY = 'test-django-oidc'
    SOCIAL_AUTH_KEYCLOAK_SECRET = 'a7a41-245e-...'
    SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = \
        'MIIBIjANBxxxdSD'
    SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = \
        'https://iam.example.com/auth/realms/voxcloud-staff/protocol/openid-connect/auth'
    SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = \
        'https://iam.example.com/auth/realms/voxcloud-staff/protocol/openid-connect/token'
      
Lastly you need to ensure the ``client_id`` is in your JWT's ``aud`` key. On your client go to Mappers -> Create. Create an ``Audience Mapper`` and ensure the ``Included Client Audience`` is your ``client_id``.

Thereafter go to: ``<app_url>/login/keycloak`` and the authorization code flow should commense.

The default behaviour is to associate users via username field, but you
       can change the key with e.g.

``SOCIAL_AUTH_KEYCLOAK_ID_KEY = 'email'`` 