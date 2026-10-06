External groups
===============

External memberships can restrict authentication and synchronize local groups.
Both capabilities are opt-in. Extraction does not grant local permissions.

Enable extraction
-----------------

For OpenID Connect, Keycloak, and Okta, select a literal claim name::

    SOCIAL_AUTH_OIDC_GROUPS_KEY = 'groups'
    SOCIAL_AUTH_KEYCLOAK_GROUPS_KEY = 'groups'
    SOCIAL_AUTH_OKTA_OAUTH2_GROUPS_KEY = 'groups'
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_GROUPS_KEY = 'groups'

Okta OAuth2 reads UserInfo; Okta OpenID Connect uses the validated ID token
first, then UserInfo with a matching subject. Configure Okta to issue the
claim. Org authorization servers require the ``groups`` scope; custom
authorization servers require any scope associated with the claim, if any.
See :doc:`backends/okta`
for backend-specific scopes and a Django synchronization example.

For Azure, use the setting corresponding to the selected authentication backend:

.. list-table:: Azure group extraction settings
   :header-rows: 1

   * - Backend class
     - Setting
   * - ``AzureADOAuth2``
     - ``SOCIAL_AUTH_AZUREAD_OAUTH2_GROUPS_KEY``
   * - ``AzureADOAuth2V2``
     - ``SOCIAL_AUTH_AZUREAD_OAUTH2_V2_GROUPS_KEY``
   * - ``AzureADTenantOAuth2``
     - ``SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_GROUPS_KEY``
   * - ``AzureADV2TenantOAuth2``
     - ``SOCIAL_AUTH_AZUREAD_V2_TENANT_OAUTH2_GROUPS_KEY``
   * - ``AzureADB2COAuth2``
     - ``SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_GROUPS_KEY``

Set the selected Azure setting to ``'roles'`` for Microsoft Entra application
roles, or ``'groups'`` for group identifiers. Configure the provider to issue
the selected claim. OIDC uses the validated ID token first, then UserInfo with
a matching subject. Claim names are literal keys; nested claim paths are not
supported.

GitLab, MediaWiki, and Discourse use ``GROUPS_ENABLED`` instead::

    SOCIAL_AUTH_GITLAB_GROUPS_ENABLED = True
    SOCIAL_AUTH_GITLAB_GROUPS_IDENTIFIER = 'full_path'

With ``GROUPS_ENABLED = True``, GitLab requests ``read_api`` automatically
unless ``read_api`` or ``api`` is already included in the requested scopes.
Enable the matching permission in the GitLab OAuth application's settings;
``read_user`` alone cannot retrieve groups.

GitLab returns full group paths by default. Set ``GROUPS_IDENTIFIER = 'id'``
for stable numeric IDs, represented as strings. Paths are readable but renames,
moves, and reuse can change authorization. Memberships are fetched from every
page on the configured ``API_URL``; visible groups without membership do not
qualify. Insufficient scope or a failed page aborts authentication.

For SAML, configure each identity provider independently::

    SOCIAL_AUTH_SAML_ENABLED_IDPS = {
        'company': {
            # Existing IdP configuration goes here.
            'attr_groups': 'https://example.com/claims/groups',
            'allow_groups': ['translators', 'reviewers'],
            'groups_map': {'translators': ['Translators']},
        },
    }

The complete SAML attribute is read; a singleton string is accepted.

Missing and empty memberships
-----------------------------

``get_user_groups(response)`` returns a list of exact, nonempty string
identifiers, with duplicates removed. ``None`` means extraction is disabled;
``[]`` means the provider reported no memberships.

A missing configured claim fails authentication by default. Providers that omit
the claim for users without assignments can explicitly enable::

    SOCIAL_AUTH_OIDC_GROUPS_MISSING_AS_EMPTY = True

SAML uses ``groups_missing_as_empty`` inside the IdP configuration. Malformed
claims always fail. Entra group overage also fails when reading groups, even
with this option enabled. There is no Microsoft Graph fallback; prefer
application roles or configure application-scoped groups.

Only trust group claims from the intended issuer and tenant. In particular,
restrict Azure's common endpoint appropriately before granting local access.

Restrict authentication
-----------------------

The existing ``auth_allowed`` pipeline step enforces ``ALLOW_GROUPS``::

    SOCIAL_AUTH_OIDC_ALLOW_GROUPS = ['translators', 'reviewers']

Membership in any listed group qualifies. Email/domain restrictions still
apply. An empty allow list imposes no group restriction. A nonempty allow list
requires enabled extraction. SAML uses per-IdP ``allow_groups``.

Existing ``SOCIAL_AUTH_CAS_ALLOW_GROUPS`` settings keep their behavior without
new extraction settings or pipeline steps. CAS reads ``groups`` when a
nonempty allow list or group mapping is configured, or when
``SOCIAL_AUTH_CAS_GROUPS_ENABLED = True`` explicitly enables extraction for a
custom pipeline. With group handling disabled, CAS ignores the group attribute
and returns ``None``. When enabled, CAS validates the membership list and
continues to treat a missing claim as empty membership.

Synchronize Django groups
-------------------------

Map external identifiers to lists of existing Django group names::

    SOCIAL_AUTH_OIDC_GROUPS_MAP = {
        'translators': ['Translators'],
        'reviewers': ['Reviewers', 'Translators'],
    }

Append ``social_core.pipeline.user.sync_groups`` after user creation and all
application authentication checks in ``SOCIAL_AUTH_PIPELINE``. Keep the existing
``social_details`` and ``auth_allowed`` steps; no extra extraction or restriction
steps are required. For example, extend the standard pipeline::

    from social_core.pipeline import DEFAULT_AUTH_PIPELINE

    SOCIAL_AUTH_PIPELINE = (
        *DEFAULT_AUTH_PIPELINE,
        'social_core.pipeline.user.sync_groups',
    )

The mapping targets define the memberships managed by this provider. Desired
memberships are added and obsolete managed memberships removed atomically.
Other groups are preserved. Manual membership in managed groups is replaced
at the next authentication. Empty memberships remove all managed memberships.

Django synchronization uses a transaction so a failed membership update rolls
back the changes. It does not lock user or group rows. Concurrent authentications
with different membership snapshots can interleave and leave a combination of
their memberships. Applications requiring serialized synchronization should
override ``strategy.sync_user_groups`` and coordinate membership updates using
their own locking policy. Synchronization does not prevent administrators from
renaming or deleting mapped groups concurrently.

An empty mapping disables synchronization. Unknown external groups grant
nothing; use ``ALLOW_GROUPS`` to restrict login independently. Missing local
groups, invalid configuration, disabled extraction with an enabled mapping,
and competing provider/IdP ownership of a local group cause errors before
membership changes. No groups are created and staff/superuser flags are not
modified. The default Django implementation requires ``auth.Group`` and an
automatically created membership table. Custom group models and explicit
intermediary models must override ``strategy.sync_user_groups`` to supply their
application-specific membership behavior. These unsupported relations are
rejected before any membership changes when synchronization is configured.

Synchronization runs during authentication, including registration and
linking. It does not provide background revocation, account deactivation, or
SCIM provisioning. Association-only backends do not synchronize memberships.

Custom strategies and pipelines
-------------------------------

``social_details`` exposes memberships as the top-level pipeline argument
``groups``, separate from profile ``details``. Partial pipelines preserve this
argument. There is no automatic external-group snapshot in association
``extra_data``.

Override ``strategy.sync_user_groups(user, groups, *, backend, response,
**kwargs)`` for application-specific behavior. ``DjangoStrategy`` supplies the
standard Django implementation. ``BaseStrategy`` rejects configured
synchronization without an implementation. Application strategies should
validate all targets before changing memberships and retain their own audit,
transaction, and permission-cache behavior.

``social_core.groups.group_sync_targets(backend, groups, response)`` returns
the desired and managed sets of local target identifiers, validating mapping
syntax and ownership across configured providers. SAML resolves its mapping
from ``response['idp_name']``. Strategies interpret local target identifiers;
for example, Weblate uses team IDs instead of Django group names.

MediaWiki and Discourse no longer return groups inside ``details``. Existing
custom consumers should enable extraction and use the ``groups`` pipeline
argument. This prevents profile updates from assigning a many-to-many field.
