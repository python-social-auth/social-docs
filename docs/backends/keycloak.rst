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

Thereafter go to: ``<app_url>/login/keycloak`` and the authorization code flow should commence.

User ID Configuration
---------------------

The default behavior is to associate users via the ``sub`` (subject) field from the
JWT token. However, you can configure which field to use as the unique user identifier
by setting::

    SOCIAL_AUTH_KEYCLOAK_ID_KEY = 'email'

This can be useful if you want to use email, username, or another field as the unique
identifier instead of the ``sub`` field.

.. warning::
    Changing the ID key after users have already authenticated will prevent them from
    logging in, as their stored ``uid`` will not match the new identifier. Configure
    this setting before users start authenticating, or perform a data migration.

See the `Configurable User ID Key`_ documentation for more information about this feature.

.. _Configurable User ID Key: ../configuration/settings.html#configurable-user-id-key
