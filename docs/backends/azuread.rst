Microsoft Entra ID and Azure AD B2C
===================================

Microsoft Entra ID was formerly Azure Active Directory. Login buttons use
the Microsoft title and logo following `Microsoft sign-in branding guidance
<https://learn.microsoft.com/en-us/entra/identity-platform/howto-add-branding-in-apps>`_.
Azure AD B2C retains its separate name. Backend identifiers and settings
prefixes remain unchanged.

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``azuread-oauth2``
     - ``social_core.backends.azuread.AzureADOAuth2``
   * - ``azuread-oauth2-v2``
     - ``social_core.backends.azuread.AzureADOAuth2V2``
   * - ``azuread-tenant-oauth2``
     - ``social_core.backends.azuread_tenant.AzureADTenantOAuth2``
   * - ``azuread-v2-tenant-oauth2``
     - ``social_core.backends.azuread_tenant.AzureADV2TenantOAuth2``
   * - ``azuread-b2c-oauth2``
     - ``social_core.backends.azuread_b2c.AzureADB2COAuth2``

User identifiers
----------------

The Azure backends use these claims as their default user identifiers:

.. list-table::
   :header-rows: 1

   * - Backend name
     - Default ID key
   * - ``azuread-oauth2``
     - ``sub``
   * - ``azuread-oauth2-v2``
     - ``sub``
   * - ``azuread-tenant-oauth2``
     - ``sub``
   * - ``azuread-v2-tenant-oauth2``
     - ``sub``
   * - ``azuread-b2c-oauth2``
     - ``sub``

Microsoft documents ``preferred_username`` and ``upn`` as mutable
human-readable identifiers that must not be used as authorization identities.
The backends therefore use ``sub``, which is immutable and pairwise unique to
an application ID. The ``oid`` claim is immutable across applications within a
tenant, but is only tenant-unique and must be combined with ``tid`` when used
across tenants.

For example, configure the v2 tenant backend to use ``sub``::

    SOCIAL_AUTH_AZUREAD_V2_TENANT_OAUTH2_ID_KEY = 'sub'

Older associations using ``upn`` or ``preferred_username`` are migrated to
``sub`` during authentication. See :doc:`../configuration/settings` for the
compatibility and strict migration policies. Because ``sub`` is pairwise,
changing the Azure application/client ID can also require an identity migration.
The ``sub``, ``oid``, and ``tid`` claims are retained in ``extra_data`` to make
future verified migrations possible. See the
`Microsoft ID token claims reference`_.

IdP Setup
---------

To configure Azure AD:

1. Log into the Azure Portal
2. Navigate to **Azure Active Directory** > **App registrations** > **New registration**
3. Configure:

   * **Name**: Your application name
   * **Redirect URI**: Select **Web** and enter ``https://your-domain.com/complete/azuread-oauth2/``

4. After registration, note the **Application (client) ID** and **Directory (tenant) ID**
5. Create a client secret:

   * Go to **Certificates & secrets** > **New client secret**
   * Copy the secret value immediately (you won't be able to see it again)

6. Configure API Permissions:

   * Go to **API permissions** > **Add a permission** > **Microsoft Graph**
   * Add delegated permissions: ``User.Read``, ``email``, ``openid``, ``profile``
   * Click **Grant admin consent** if required

Application Configuration
-------------------------

Fill in ``Client ID`` and ``Client Secret`` settings with values from Azure AD::

    SOCIAL_AUTH_AZUREAD_OAUTH2_KEY = ''
    SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_AZUREAD_OAUTH2_RESOURCE = ''

  This is the resource you would like to access after authentication succeeds.
  Some of the possible values are: ``https://graph.windows.net`` or
  ``https://<your Sharepoint site name>-my.sharepoint.com``.

  When using Microsoft Graph, the resource needed is::

      SOCIAL_AUTH_AZUREAD_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'

- Add the backend to the authentication backends setting::

      AUTHENTICATION_BACKENDS = (
          ...
          'social_core.backends.azuread.AzureADOAuth2',
          ...
      )

- If you are using an authority host other than the default ``AZURE_PUBLIC_CLOUD`` (``'login.microsoftonline.com'``)
  then you can override the default with the  ``AUTHORITY_HOST`` setting. A list of Azure authority hosts can be found
  in the `Azure Authority Hosts`_ doc::

      SOCIAL_AUTH_AZUREAD_OAUTH2_AUTHORITY_HOST = ''

- Federated identity credentials (client assertions) are supported when you do not want to use a client secret. After
  adding a federated credential to your Entra ID app, point the backend at the OIDC token that your workload issues
  (for example, Kubernetes service account tokens issued via Azure Workload Identity, or other OIDC tokens where you manage
  writing the token to a file). Precedence: if ``SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET`` is set, the backend uses the client
  secret and does not send a client assertion; otherwise it prefers an explicit ``SOCIAL_AUTH_AZUREAD_OAUTH2_CLIENT_ASSERTION``;
  if no assertion is provided, it reads a token file from ``AZURE_FEDERATED_TOKEN_FILE`` (or ``OAUTH2_FEDERATED_TOKEN_FILE``) or
  ``SOCIAL_AUTH_AZUREAD_OAUTH2_FEDERATED_TOKEN_FILE``. The backend will automatically use a client assertion instead of
  ``CLIENT_SECRET`` when the secret is omitted.

  Default path used by Azure Workload Identity on Kubernetes::

      AZURE_FEDERATED_TOKEN_FILE=/var/run/secrets/azure/tokens/azure-identity-token

  Or configure explicitly via the backend setting::

      SOCIAL_AUTH_AZUREAD_OAUTH2_FEDERATED_TOKEN_FILE = '/path/to/oidc/token'

  You can also provide a pre-built client assertion JWT (preferred when you already create the assertion yourself)::

      SOCIAL_AUTH_AZUREAD_OAUTH2_CLIENT_ASSERTION = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...'
      # Optional: defaults to the standard JWT bearer URN shown here
      SOCIAL_AUTH_AZUREAD_OAUTH2_CLIENT_ASSERTION_TYPE = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'

  Minimal configs by approach:

  - Token file (workload-issued OIDC token): leave ``SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET`` unset; set either
    ``AZURE_FEDERATED_TOKEN_FILE`` (or ``OAUTH2_FEDERATED_TOKEN_FILE``) or ``SOCIAL_AUTH_AZUREAD_OAUTH2_FEDERATED_TOKEN_FILE``
    to the token path. ``CLIENT_ASSERTION_TYPE`` is not needed for this mode.

  - Pre-built client assertion: leave ``SOCIAL_AUTH_AZUREAD_OAUTH2_SECRET`` unset; set
    ``SOCIAL_AUTH_AZUREAD_OAUTH2_CLIENT_ASSERTION`` (and optionally ``SOCIAL_AUTH_AZUREAD_OAUTH2_CLIENT_ASSERTION_TYPE``
    if you use a non-standard type). ``FEDERATED_TOKEN_FILE`` is not read in this mode because the explicit assertion wins.

  Kubernetes projected service account token volume example::

      apiVersion: v1
      kind: Pod
      metadata:
        name: mypod
      spec:
        serviceAccountName: myserviceaccount
        containers:
        - name: mycontainer
          image: myimage
          env:
          - name: AZURE_FEDERATED_TOKEN_FILE
            value: /var/run/secrets/azure/tokens/azure-identity-token
          volumeMounts:
          - name: azure-identity-token
            mountPath: /var/run/secrets/azure/tokens
            readOnly: true
        volumes:
        - name: azure-identity-token
          projected:
            sources:
            - serviceAccountToken:
              path: azure-identity-token
              audience: api://AzureADTokenExchange
              expirationSeconds: 3600

  These settings apply to Azure AD/Entra ID scenarios. For more information on workload identity, see `Workload Identity Federation`_ and `Federated identity credentials (Workload Identity)`_.

Authority configuration
-----------------------

Use ``AUTHORITY_URL`` to choose the host and sign-in audience together. For
example, restrict sign-in to work and school accounts with::

    SOCIAL_AUTH_AZUREAD_OAUTH2_AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'

The audience path is ``common`` for work, school, and personal Microsoft accounts,
``organizations`` for work and school accounts, or ``consumers`` for personal
accounts. A tenant UUID or tenant domain selects a specific tenant. The app
registration must also allow the chosen account types. See
`Microsoft authorization code flow`_.

Specify an HTTPS base authority, including its audience or tenant path. Omit
``/oauth2/authorize``, ``/oauth2/token``, ``/v2.0``, and discovery suffixes. The
backend class selects v1 or v2 endpoints. Trailing slashes are normalized;
credentials, query strings, and fragments are not accepted.

Each backend has its own configuration prefix:

.. list-table::
   :header-rows: 1

   * - Backend
     - Authority setting
   * - ``azuread-oauth2``
     - ``SOCIAL_AUTH_AZUREAD_OAUTH2_AUTHORITY_URL``
   * - ``azuread-oauth2-v2``
     - ``SOCIAL_AUTH_AZUREAD_OAUTH2_V2_AUTHORITY_URL``
   * - ``azuread-tenant-oauth2``
     - ``SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_AUTHORITY_URL``
   * - ``azuread-v2-tenant-oauth2``
     - ``SOCIAL_AUTH_AZUREAD_V2_TENANT_OAUTH2_AUTHORITY_URL``
   * - ``azuread-b2c-oauth2``
     - ``SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_AUTHORITY_URL``

For example, use the v2 backend for organizational accounts::

    SOCIAL_AUTH_AZUREAD_OAUTH2_V2_AUTHORITY_URL = 'https://login.microsoftonline.com/organizations'

Or use a tenant backend with an explicit authority::

    SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_AUTHORITY_URL = 'https://login.microsoftonline.com/your-tenant.onmicrosoft.com'
    SOCIAL_AUTH_AZUREAD_V2_TENANT_OAUTH2_AUTHORITY_URL = 'https://login.microsoftonline.com/your-tenant.onmicrosoft.com'

An explicit authority supplies the base for authorization, token exchange,
refresh, and discovery. Without it, existing ``AUTHORITY_HOST``, ``TENANT_ID``,
and ``TENANT_NAME`` configuration continues to work. A UUID ``TENANT_ID`` in a
tenant backend remains a token validation restriction even when the authority
is overridden. Individual ``AUTHORIZATION_URL``, ``ACCESS_TOKEN_URL``, and
``OPENID_CONFIGURATION_URL`` overrides take precedence over the derived URLs.
Token issuer, signing-key, tenant, and B2C policy validation remain enabled.

For B2C custom domains, end the authority at the tenant domain and configure
the policy separately::

    SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_TENANT_NAME = 'your-tenant'
    SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_AUTHORITY_URL = 'https://login.example.com/your-tenant.onmicrosoft.com'
    SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_POLICY = 'b2c_1_signin'

The backend retains its policy query parameters; do not append the policy to
``AUTHORITY_URL``.

Proof Key for Code Exchange (PKCE)
----------------------------------

All five Azure backends support PKCE. It is disabled by default to preserve
existing integrations. Enable it with the selected backend's setting::

    SOCIAL_AUTH_AZUREAD_OAUTH2_USE_PKCE = True
    # For the other backends, use the corresponding setting instead:
    SOCIAL_AUTH_AZUREAD_OAUTH2_V2_USE_PKCE = True
    SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_USE_PKCE = True
    SOCIAL_AUTH_AZUREAD_V2_TENANT_OAUTH2_USE_PKCE = True
    SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_USE_PKCE = True

The default challenge method is ``S256``. The backend saves a random verifier
in the session, sends its SHA-256 challenge at authorization, and sends the
verifier when redeeming the code. PKCE complements client authentication;
continue to configure a client secret or federated assertion for confidential
clients. V2 backends are recommended for new integrations.

Register server-side callbacks as **Web** redirect URIs, including applications
with a separate frontend. Enabling PKCE alone does not make a server-side flow
compatible with an Azure **SPA** registration: Microsoft also requires an
``Origin`` header for SPA token redemption and restricts client credentials
when that header is present. See `Microsoft authorization code flow`_.

Token renewal
-------------

``backend.get_auth_token(user_id)`` returns the stored access token and renews
it when its stored expiry indicates it has expired. Renewal requires a stored
refresh token. If the token is expired and no refresh token is available, it
raises ``AuthCredentialError`` with ``code='reauthentication_required'`` and
``stage='refresh'`` instead of returning the expired token. Arrange another
provider login to obtain new credentials. See :ref:`oauth-token-renewal` for
the shared renewal behavior.

Tenant Support
--------------

If the app is linked to a specific tenant (vs the common tenant) it's
possible to use a version of the backend with tenant support.

IdP Setup for Tenant
^^^^^^^^^^^^^^^^^^^^^

Follow the same IdP setup steps from the 'IdP Setup' section above, but use redirect URI::

    https://your-domain.com/complete/azuread-tenant-oauth2/

Application Configuration for Tenant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Fill in ``Client ID``, ``Client Secret``, and ``Tenant ID`` settings::

    SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = ''
    SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = ''
    SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_TENANT_ID = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_RESOURCE = ''

  This is the resource you would like to access after authentication succeeds.
  Some of the possible values are: ``https://graph.windows.net`` or
  ``https://<your Sharepoint site name>-my.sharepoint.com``.

  When using Microsoft Graph, the resource needed is::

      SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'

- Add the backend to the authentication backends setting::

      AUTHENTICATION_BACKENDS = (
          ...
          'social_core.backends.azuread_tenant.AzureADTenantOAuth2',
          ...
      )

- If you are using an authority host other than the default ``AZURE_PUBLIC_CLOUD`` ('login.microsoftonline.com')
  then you can override the default with the  ``AUTHORITY_HOST`` setting. The Azure authority hosts are listed
  in the `Azure Authority Hosts`_ doc::

      SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_AUTHORITY_HOST = ''

B2C Tenant
----------
If the app needs custom business logic for authentication then use the Azure AD B2C tenant.

To enable OAuth2 B2C Tenant support:

- Fill in ``Client ID`` and ``Client Secret`` settings. These values can be
  obtained easily as described in `Azure AD Application Registration`_ doc::

      SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_KEY = ''
      SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_SECRET = ''

- Fill in the tenant name (without ``.onmicrosoft.com``)::

      SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_TENANT_NAME = ''

- Fill in the B2C policy::

      SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_POLICY = ''

The policy should start with `b2c_`. For more information see `Azure AD B2C User flows and custom policies overview`_ doc.

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_RESOURCE = ''

  This is the resource you would like to access after authentication succeeds.
  Some of the possible values are: ``https://graph.windows.net`` or
  ``https://<your Sharepoint site name>-my.sharepoint.com``.

  When using Microsoft Graph, the resource needed is::

      SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'

- Add the backend to the authentication backends setting::

      AUTHENTICATION_BACKENDS = (
          ...
          'social_core.backends.azuread_b2c.AzureADB2COAuth2',
          ...
      )

- If you are using an authority host other than the default ``AZURE_PUBLIC_CLOUD`` ('b2clogin.com')
  then you can override the default with the  ``AUTHORITY_HOST`` setting.

      SOCIAL_AUTH_AZUREAD_B2C_OAUTH2_AUTHORITY_HOST = ''


.. _azure-b2c-logout:

B2C provider logout
-------------------

``AzureADB2COAuth2.logout_url()`` returns the provider logout URL from the
configured policy's OpenID Connect ``end_session_endpoint``. It preserves
endpoint query parameters and includes the configured client ID. It does not
send a request or clear the application's session.

The optional keyword arguments are ``post_logout_redirect_uri``,
``id_token_hint``, and ``state``. Pass the previously issued ID token from
``extra_data`` as the hint. Configure a trusted return URL and register it with
your B2C application. When B2C requires an ID token for logout, it checks the
return URL against registered redirect URIs. If using ``state``, save it and
verify it on the return callback. See `Microsoft B2C sign-out`_.

Build the URL using the same policy that authenticated the user. For example,
a Django view can retrieve the token before clearing the local session:

.. code-block:: python

    from django.contrib.auth import logout
    from django.contrib.auth.decorators import login_required
    from django.shortcuts import redirect
    from django.views.decorators.http import require_POST
    from social_django.utils import load_backend, load_strategy

    @login_required
    @require_POST
    def b2c_logout(request):
        social = request.user.social_auth.get(provider='azuread-b2c-oauth2')
        strategy = load_strategy(request)
        backend = load_backend(
            strategy, 'azuread-b2c-oauth2', redirect_uri=None
        )
        provider_url = backend.logout_url(
            post_logout_redirect_uri=request.build_absolute_uri('/signed-out/'),
            id_token_hint=social.extra_data.get('id_token'),
        )
        logout(request)
        return redirect(provider_url)

Use a CSRF-protected POST form to invoke this view. This example assumes an
authenticated B2C user and a single configured sign-in policy. Applications
with multiple policies must select the backend for the stored sign-in policy.
A missing or invalid ``end_session_endpoint`` raises ``AuthResponseError``
with ``code="missing_claim"`` or ``code="invalid_claim"``, respectively;
discovery request failures propagate through the usual backend error handling.

Provider logout complements local logout. Disconnecting an account removes
its association instead; see :doc:`../logging_out`.

.. _Azure AD Application Registration: https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app
.. _Azure AD B2C User flows and custom policies overview: https://docs.microsoft.com/en-us/azure/active-directory-b2c/user-flow-overview
.. _Azure Authority Hosts: https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.azureauthorityhosts?view=azure-python
.. _Workload Identity Federation: https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation
.. _Federated identity credentials (Workload Identity): https://azure.github.io/azure-workload-identity/docs/topics/federated-identity-credential.html
.. _Microsoft ID token claims reference: https://learn.microsoft.com/en-us/entra/identity-platform/id-token-claims-reference

.. _Microsoft authorization code flow: https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
.. _Microsoft B2C sign-out: https://learn.microsoft.com/en-us/azure/active-directory-b2c/openid-connect#send-a-sign-out-request

External memberships
--------------------

See :doc:`/groups` for opt-in extraction, group-based login restrictions, and
local group synchronization. No separate extraction pipeline step is needed.
