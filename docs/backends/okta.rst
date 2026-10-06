Okta
====

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``okta-oauth2``
     - ``social_core.backends.okta.OktaOAuth2``
   * - ``okta-openidconnect``
     - ``social_core.backends.okta_openidconnect.OktaOpenIdConnect``

This section describes how to setup the different services provided by Okta.

Okta OAuth2
-----------

IdP Setup
^^^^^^^^^

To configure Okta for OAuth2:

1. Log into your Okta Admin Console
2. Navigate to **Applications** > **Create App Integration**
3. Select **OIDC - OpenID Connect** and **Web Application**
4. Set the **Sign-in redirect URI** to::

    https://your-domain.com/complete/okta-oauth2/

5. Save and note the **Client ID**, **Client Secret**, and **Okta domain** (e.g., ``https://dev-123456.okta.com``)

.. important::
   Do NOT use the ``/oauth2/default`` endpoint for Okta authentication.

Application Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

Fill ``Client ID``, ``Client Secret`` and ``API URL (e.g.
https://dev-123456.okta.com/oauth2)`` settings with the values from the IdP setup above::

    SOCIAL_AUTH_OKTA_OAUTH2_KEY = ''
    SOCIAL_AUTH_OKTA_OAUTH2_SECRET = ''
    SOCIAL_AUTH_OKTA_OAUTH2_API_URL = ''

Okta OpenID Connect
-------------------

IdP Setup
^^^^^^^^^

Follow the same steps as OAuth2 above, but use the redirect URI::

    https://your-domain.com/complete/okta-openidconnect/

Application Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

Fill ``Client ID``, ``Client Secret`` and ``API URL (e.g.
https://dev-123456.okta.com/oauth2)`` settings with the values from the IdP setup::

    SOCIAL_AUTH_OKTA_OPENIDCONNECT_KEY = ''
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_SECRET = ''
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_API_URL = ''

Scopes and external groups
--------------------------

Both backends request ``openid``, ``profile``, and ``email`` by default.
For the org authorization server (``/oauth2/v1/authorize``), request the
``groups`` scope with the setting matching your backend::

    # social_core.backends.okta.OktaOAuth2
    SOCIAL_AUTH_OKTA_OAUTH2_SCOPE = ['groups']

    # social_core.backends.okta_openidconnect.OktaOpenIdConnect
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_SCOPE = ['groups']

These settings add to the default scopes. ``SOCIAL_AUTH_OIDC_SCOPE`` applies
only to the generic OpenID Connect backend.

For a custom authorization server (``/oauth2/{authorizationServerId}/v1/authorize``,
including ``default``), ``groups`` is not an automatically defined scope.
Configure the groups claim for any scope or for specific scopes, then request
any scope associated with that claim using the matching ``SCOPE`` setting.
If the claim is available with the default scopes, no additional scope is
needed; Okta's custom-server example requests only ``openid``. Request
``groups`` only if you have defined that scope on the custom server and
associated it with the claim; requesting an undefined scope causes
``invalid_scope``.

Configure Okta to issue a groups claim with an appropriate group filter;
requesting a scope alone does not configure the claim. See
`Okta's groups claim guide <https://developer.okta.com/docs/guides/customize-tokens-groups-claim/main/>`_
for org and custom authorization server configuration.

Group extraction and local synchronization are opt-in. For ``OktaOAuth2``,
configure the literal claim name and map external groups to existing Django
group names::

    SOCIAL_AUTH_OKTA_OAUTH2_GROUPS_KEY = 'groups'
    SOCIAL_AUTH_OKTA_OAUTH2_GROUPS_MAP = {
        'engineering': ['Engineering'],
    }

    from social_core.pipeline import DEFAULT_AUTH_PIPELINE

    SOCIAL_AUTH_PIPELINE = (
        *DEFAULT_AUTH_PIPELINE,
        'social_core.pipeline.user.sync_groups',
    )

For ``OktaOpenIdConnect``, use the corresponding settings with the same
pipeline::

    SOCIAL_AUTH_OKTA_OPENIDCONNECT_GROUPS_KEY = 'groups'
    SOCIAL_AUTH_OKTA_OPENIDCONNECT_GROUPS_MAP = {
        'engineering': ['Engineering'],
    }

``OktaOAuth2`` reads the claim from UserInfo. ``OktaOpenIdConnect`` prefers the
validated ID token and falls back to UserInfo only when its subject matches
the ID token. Enabling extraction does not automatically request additional
scopes.

Synchronization adds desired mapped memberships and removes obsolete mapped
memberships, preserving unrelated Django groups. It does not create groups.
An empty claim clears managed memberships; a missing configured claim fails
authentication by default. If Okta omits the claim for users with no groups,
explicitly set ``SOCIAL_AUTH_OKTA_OAUTH2_GROUPS_MISSING_AS_EMPTY = True`` or
``SOCIAL_AUTH_OKTA_OPENIDCONNECT_GROUPS_MISSING_AS_EMPTY = True`` for your
backend. Malformed claims still fail authentication.

See :doc:`../groups` for validation, authentication restrictions, and
synchronization behavior.

User identification
-------------------

Both Okta backends identify users by the stable ``sub`` claim. Associations
created by older social-core releases used ``preferred_username`` and migrate
to ``sub`` on the next successful authentication. See `Configurable User ID
Key`_ for migration controls and custom identifier settings.

.. _Configurable User ID Key: ../configuration/settings.html#configurable-user-id-key
