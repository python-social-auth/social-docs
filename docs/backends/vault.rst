Hashicorp Vault
===============

The Vault_ backend allows authentication against the OIDC provider_ in
Hashicorp Vault_ version 1.9 and later.

The backend class is `VaultOpenIdConnect` with name `vault`.  A minimum
configuration is::

    SOCIAL_AUTH_VAULT_OIDC_ENDPOINT = 'https://vault.example.net:8200/v1/identity/oidc/provider/default'
    SOCIAL_AUTH_VAULT_KEY = '<client_id>'
    SOCIAL_AUTH_VAULT_SECRET = '<client_secret>'

The remaining configuration will be auto-detected, by fetching::

    <SOCIAL_AUTH_VAULT_OIDC_ENDPOINT>/.well-known/openid-configuration

You may need to set ``SOCIAL_AUTH_VAULT_VERIFY_SSL = False`` if your Vault
server does not have its certificate signed by a trusted CA (e.g.  with
LetsEncrypt), although this should only be used for testing and not in
production.

Vault OIDC configuration
------------------------

Vault 1.10 onwards includes a pre-defined provider "default", key "default"
and assignment "allow_all".  With Vault 1.9 you will need to create these
objects explicitly.

You can then create an OIDC client, and read it back to get the auto-generated
client ID and secret::

    vault write identity/oidc/client/my-app \
        redirect_uris="https://www.example.com/callback" \
        assignments="allow_all" \
        key="default" \
        id_token_ttl="30m" \
        access_token_ttl="1h"

    vault read identity/oidc/client/my-app

Scopes
------

Vault is very flexible with regard to configuring claims and scopes,
so it's up to you how you map entity and/or alias metadata to OIDC claims.
Here is a suggestion, which exposes the entity name as "preferred_username"
and takes the other claims from entity metadata::

    vault write identity/oidc/scope/profile \
      description="Provides user info" \
      template='{
        "preferred_username": {{identity.entity.name}},
        "name": {{identity.entity.metadata.name}},
        "given_name": {{identity.entity.metadata.given_name}},
        "family_name": {{identity.entity.metadata.family_name}}
    }'

    vault write identity/oidc/scope/email \
      description="Provides email address" \
      template='{
        "email": {{identity.entity.metadata.email}}
    }'

    vault write identity/oidc/scope/groups \
      description="Provides a list of group names" \
      template='{
        "groups": {{identity.entity.groups.names}}
    }'

The Vault backend inherits defaults from ``open_id_connect.py``.  In
particular, it looks for the username in the ``preferred_username`` claim.
If you need to choose a different claim then you can do so::

    SOCIAL_AUTH_VAULT_USERNAME_KEY = 'nickname'

The default set of scopes requested are "openid", "profile" and "email".
You can request additional claims like this::

    SOCIAL_AUTH_VAULT_SCOPE = ['groups']

and you can remove the default scopes using::

    SOCIAL_AUTH_VAULT_IGNORE_DEFAULT_SCOPE = True

.. _Vault: https://www.vaultproject.io/
.. _provider: https://www.vaultproject.io/docs/secrets/identity/oidc-provider
