Weblate
========

Backend class
-------------

For Django, add ``social_core.backends.weblate.WeblateOpenIdConnect`` to
``AUTHENTICATION_BACKENDS``. For other integrations, use the same class path in
the framework-specific backend setting. The backend name is ``weblate``.

This backend authenticates against Weblate's optional OpenID Connect identity
provider, introduced in Weblate 2026.11. See the
`Weblate identity provider documentation`_ for server setup.

Register a confidential authorization-code client with RSA SHA-256 signing on
the Weblate server. Register your application's exact HTTPS callback URL,
typically ``https://your-domain.com/complete/weblate/``, and configure::

    SOCIAL_AUTH_WEBLATE_KEY = '<client_id>'
    SOCIAL_AUTH_WEBLATE_SECRET = '<client_secret>'

The default issuer is ``https://hosted.weblate.org/oidc``. Discovery supplies the
authorization, token, UserInfo, and signing-key endpoints. The backend uses
authorization code flow with S256 PKCE enabled by default, as required by Weblate,
and requests ``openid profile email`` scopes. Keep PKCE enabled.

Custom installations
--------------------

Configure another Weblate issuer with::

    SOCIAL_AUTH_WEBLATE_OIDC_ENDPOINT = 'https://weblate.example.com/oidc'

Include any deployment prefix before ``/oidc``, for example
``https://example.com/translations/oidc``. Do not append
``/.well-known/openid-configuration``. Trailing slashes are normalized.
Settings use the usual per-backend and global precedence described in
:doc:`../configuration/settings`.

The settings-aware sign-in label is **Hosted Weblate** when the effective issuer
hostname is exactly ``hosted.weblate.org``, and **Weblate** otherwise. Both use
the official Weblate icon. Integrations retrieve the label using
``WeblateOpenIdConnect.get_title(strategy)``; Django's backend metadata context
processor uses this interface when available. The static ``title`` attribute
remains the default label.

Account bindings use the stable ``sub`` claim, not the username or e-mail address.
Changing the issuer changes the identity authority within the same ``weblate``
backend namespace. Plan an explicit migration of existing associations before
switching installations: equal numeric subjects on different servers do not
identify the same person. SAML identities are not automatically migrated or
linked by matching e-mail addresses.

Legal-version claim
-------------------

When the provider has Weblate's legal module installed, request the additional
scope with::

    SOCIAL_AUTH_WEBLATE_SCOPE = ['weblate:legal']

This adds to the default scopes. The backend stores a returned
``weblate_tos_version`` claim in the association's ``extra_data`` under the same
name, for example ``'2026-09-01'``. The claim is omitted when the provider has no
recorded acceptance. Previously accepted versions are stored unchanged.
If the legal module is unavailable, do not request this scope.

The claim records a provider assertion, not local acceptance. Receiving
applications must explicitly trust the issuer and match its accepted version to
their own legal documents before suppressing a local confirmation. This backend
does not accept terms on behalf of users.

.. _Weblate identity provider documentation: https://docs.weblate.org/en/latest/admin/auth.html#oidc-provider
