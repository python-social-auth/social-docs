Microsoft Azure Active Directory
================================

To enable OAuth2 support:

- Fill in ``Client ID`` and ``Client Secret`` settings. These values can be
  obtained easily as described in `Azure AD Application Registration`_ doc::

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
      (for example, Kubernetes service account tokens, GitHub Actions OIDC tokens, or Azure Workload Identity). The backend
      will automatically use a client assertion instead of ``CLIENT_SECRET`` when the secret is omitted::

            # Default path exported by Azure Workload Identity and GitHub Actions
            AZURE_FEDERATED_TOKEN_FILE=/var/run/secrets/azure/tokens/azure-identity-token

            # Or configure explicitly via the backend setting
            SOCIAL_AUTH_AZUREAD_OAUTH2_FEDERATED_TOKEN_FILE = '/path/to/oidc/token'

      You can also provide a pre-built client assertion JWT::

            SOCIAL_AUTH_AZUREAD_OAUTH2_CLIENT_ASSERTION = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...'
            SOCIAL_AUTH_AZUREAD_OAUTH2_CLIENT_ASSERTION_TYPE = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'

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

      These settings apply to all Azure AD/Entra ID variants in this doc (common, tenant-specific, v2, and B2C). For more
      information on workload identity, see `Workload Identity Federation`_ and `Federated identity credentials (Workload Identity)`_ docs.

Tenant Support
--------------

If the app is linked to a specific tenant (vs the common tenant) it's
possible to use a version of the backend with tenant support.

*Note: The backends are split because of the needed cryptography dependencies which must be installed manually.*

To enable OAuth2 Tenant support:

- Fill in ``Client ID`` and ``Client Secret`` settings. These values can be
  obtained easily as described in `Azure AD Application Registration`_ doc::

      SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_KEY = ''
      SOCIAL_AUTH_AZUREAD_TENANT_OAUTH2_SECRET = ''

- Fill in the tenant id::

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

- Fill in the tenant id::

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

.. _Azure AD Application Registration: https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app
.. _Azure AD B2C User flows and custom policies overview: https://docs.microsoft.com/en-us/azure/active-directory-b2c/user-flow-overview
.. _Azure Authority Hosts: https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.azureauthorityhosts?view=azure-python
.. _Federated identity credentials: https://learn.microsoft.com/en-us/graph/api/resources/federatedidentitycredentials-overview
.. _Workload Identity Federation: https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation
.. _Federated identity credentials (Workload Identity): https://azure.github.io/azure-workload-identity/docs/topics/federated-identity-credential.html
