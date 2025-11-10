Keycloak - Open Source Red Hat SSO
==================================

Keycloak is an open source IAM and SSO system.

IdP Setup
---------

To configure Keycloak:

1. Log into your Keycloak Admin Console and select your Realm
2. Navigate to **Clients** > **Create**
3. Configure the client:

   * **Client ID**: Choose a meaningful name (e.g., ``django-app``)
   * **Client Protocol**: ``openid-connect``
   * **Access Type**: ``confidential``
   * **Valid Redirect URIs**: ``https://your-domain.com/complete/keycloak/``

4. Save and go to the **Credentials** tab to get the **Client Secret**
5. Under **Fine Grain OpenID Connect Configuration**, set:

   * **User Info Signed Response Algorithm**: ``RS256``
   * **Request Object Signature Algorithm**: ``RS256``

6. Get the public key from **Realm Settings** > **Keys** > **RS256**
7. Create an **Audience Mapper** (**Mappers** > **Create**) to ensure your ``client_id`` is in the JWT's ``aud`` claim
8. Note the **Authorization URL** and **Token URL** from the Realm OpenID Endpoint Configuration

Application Configuration
-------------------------

Add Keycloak to your ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.keycloak.KeycloakOAuth2',
        'django.contrib.auth.backends.ModelBackend',
    )

Configure with values from your Keycloak client::

    SOCIAL_AUTH_KEYCLOAK_KEY = 'test-django-oidc'
    SOCIAL_AUTH_KEYCLOAK_SECRET = 'a7a41-245e-...'
    SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY = \
        'MIIBIjANBxxxdSD'
    SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL = \
        'https://iam.example.com/auth/realms/voxcloud-staff/protocol/openid-connect/auth'
    SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL = \
        'https://iam.example.com/auth/realms/voxcloud-staff/protocol/openid-connect/token'

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
