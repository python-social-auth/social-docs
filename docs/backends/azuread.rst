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


Tenant Support
--------------

If the app is linked to a specific tenant (vs the common tenant) it's
possible to use a version of the backend with tenant support.

*Note: The backend are split because of the needed cryptography
       dependencies which must be installed manually.*


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

      SOCIAL_AUTH_AZUREAD_OAUTH2_RESOURCE = 'https://graph.microsoft.com/'

- Add the backend to the authentication backends setting::

      AUTHENTICATION_BACKENDS = (
          ...
          'social_core.backends.azuread_tenant.AzureADTenantOAuth2',
          ...
      )

.. _Azure AD Application Registration: https://msdn.microsoft.com/en-us/library/azure/dn132599.aspx
