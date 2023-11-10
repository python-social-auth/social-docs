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

