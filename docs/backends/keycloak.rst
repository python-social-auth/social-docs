Keycloak - Open Source Red Hat SSO
==================================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``keycloak``
     - ``social_core.backends.keycloak.KeycloakOAuth2``

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
5. Under **Fine Grain OpenID Connect Configuration** (found in the client's Settings or Advanced Settings tab; location may vary depending on Keycloak version), set:

   * **User Info Signed Response Algorithm**: ``RS256``
   * **Request Object Signature Algorithm**: ``RS256``

6. Get the active public key from **Realm Settings** > **Keys** > **RS256**
7. Create an **Audience Mapper** for the client to ensure its **Client ID** is
   included in the access token's ``aud`` claim. In recent Keycloak versions,
   navigate to **Client scopes** > ``<client-id>-dedicated`` > **Add mapper** >
   **Audience**, select the client under **Included Client Audience**, and enable
   **Add to access token**.
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

Audience validation
-------------------

``SOCIAL_AUTH_KEYCLOAK_KEY`` is the OAuth **Client ID**. The backend also uses
this value as the expected audience when validating the access token. Therefore,
the exact value configured in ``SOCIAL_AUTH_KEYCLOAK_KEY`` must be present in the
token's ``aud`` claim.

The ``azp`` (authorized party) claim does not satisfy audience validation. For
example, with ``SOCIAL_AUTH_KEYCLOAK_KEY = 'test-django-oidc'``, the access token
should contain claims similar to::

    {
        "azp": "test-django-oidc",
        "aud": ["test-django-oidc"]
    }

If the Client ID is missing from ``aud``, configure the Audience Mapper described
above. Otherwise, authentication fails with an audience validation error even
when ``azp`` identifies the correct client.

Signing key rotation
--------------------

The Keycloak backend verifies access tokens with the single static key configured
in ``SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY``. It does not use the JWT header's ``kid``
(key ID) to select a key and does not fetch keys from Keycloak's JWKS endpoint.

The configured key must therefore be the active RS256 signing key from the same
realm that issues the token. After a realm signing-key rotation, update
``SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY``; otherwise, authentication fails with a
signature verification error. The token's ``kid`` can be compared with the key
ID shown under **Realm Settings** > **Keys** to diagnose a mismatch.

For automatic signing-key discovery and rotation, consider using the generic
:doc:`oidc` backend instead. It uses OpenID Connect discovery, selects keys from
the provider's JWKS by ``kid``, and refreshes the JWKS when a new key appears.

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
