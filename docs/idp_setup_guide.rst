Identity Provider (IdP) Setup Guide
====================================

This guide helps Identity Provider (IdP) administrators configure their systems to work with applications using Python Social Auth, particularly for OIDC (OpenID Connect) and SSO (Single Sign-On) implementations.

.. contents:: Table of Contents
   :local:
   :depth: 2

Overview
--------

When integrating your application with an Identity Provider for authentication, the IdP administrator needs to configure several settings. This guide provides the essential information needed to complete that setup.

Understanding the Redirect URI / Callback URL
----------------------------------------------

The **Redirect URI** (also called **Callback URL**) is the most critical configuration setting. After a user successfully authenticates with the IdP, they are redirected back to your application at this URL.

**Format:**

For most backends, the redirect URI follows this pattern::

    https://your-domain.com/complete/<backend-name>/

**Examples:**

* OIDC (generic): ``https://example.com/complete/oidc/``
* Okta OAuth2: ``https://example.com/complete/okta-oauth2/``
* Okta OpenID Connect: ``https://example.com/complete/okta-openidconnect/``
* Auth0 OpenID Connect: ``https://example.com/complete/auth0-openidconnect/``
* Azure AD: ``https://example.com/complete/azuread-oauth2/`` or ``https://example.com/complete/azuread-tenant-oauth2/``
* Keycloak: ``https://example.com/complete/keycloak/``
* Google OAuth2: ``https://example.com/complete/google-oauth2/``
* GitHub: ``https://example.com/complete/github/``

.. note::
   Replace ``https://example.com`` with your actual application domain.
   If your application is running on a different path or port, adjust accordingly.
   For development: ``http://localhost:8000/complete/<backend-name>/``

.. warning::
   The redirect URI must use **HTTPS** in production environments.
   Most IdPs will reject HTTP URLs for security reasons.

Required Information from Application Developers
-------------------------------------------------

Before starting the IdP configuration, gather this information from your application development team:

1. **Backend Name**: Which authentication backend is being used (e.g., ``oidc``, ``okta-openidconnect``, ``keycloak``)
2. **Application Domain**: The full domain where the application is hosted
3. **Required Scopes**: What user information the application needs (typically: ``openid``, ``profile``, ``email``)
4. **Additional Settings**: Any backend-specific requirements

Generic OIDC Provider Setup
----------------------------

For a generic OpenID Connect provider, follow these steps:

1. **Create a new Application/Client**

   * Choose "Web Application" as the application type
   * Note the ``Client ID`` and ``Client Secret`` generated

2. **Configure the Redirect URI**

   Set the redirect URI to::

       https://your-domain.com/complete/oidc/

3. **Configure Scopes/Permissions**

   Enable at least these scopes:

   * ``openid`` - Required for OpenID Connect
   * ``profile`` - User profile information
   * ``email`` - User email address

4. **OIDC Discovery Endpoint**

   Ensure your IdP exposes the OpenID Connect discovery endpoint::

       https://your-idp-domain/.well-known/openid-configuration

   The Python Social Auth backend will automatically discover endpoints from this URL.

5. **Provide to Development Team**

   Give these values to your application developers:

   * ``Client ID``
   * ``Client Secret``
   * ``OIDC Endpoint`` (e.g., ``https://your-idp-domain``)

Provider-Specific Setup Guides
-------------------------------

Okta
****

**OAuth2 Setup:**

1. Log into your Okta Admin Console
2. Navigate to **Applications** > **Create App Integration**
3. Select **OIDC - OpenID Connect** and **Web Application**
4. Configure:

   * **App integration name**: Your application name
   * **Sign-in redirect URIs**: ``https://your-domain.com/complete/okta-oauth2/``
   * **Assignments**: Select which users/groups can access

5. Save and note:

   * **Client ID**
   * **Client Secret**
   * **Okta domain** (e.g., ``https://dev-123456.okta.com``)

**OpenID Connect Setup:**

Same as OAuth2 above, but use redirect URI::

    https://your-domain.com/complete/okta-openidconnect/

.. important::
   Do NOT use the ``/oauth2/default`` endpoint for Okta authentication.
   Use your full Okta domain (e.g., ``https://dev-123456.okta.com/oauth2``)

Auth0
*****

1. Log into your Auth0 Dashboard
2. Navigate to **Applications** > **Create Application**
3. Select **Regular Web Applications**
4. In the application settings:

   * **Allowed Callback URLs**: ``https://your-domain.com/complete/auth0-openidconnect/``
   * **Allowed Logout URLs**: ``https://your-domain.com/logout/`` (if using logout)
   * **Allowed Web Origins**: ``https://your-domain.com``

5. In the **Settings** tab, note:

   * **Domain** (e.g., ``mytenant.auth0.com``)
   * **Client ID**
   * **Client Secret**

6. Under **Advanced Settings** > **Grant Types**, ensure these are enabled:

   * Authorization Code
   * Refresh Token (if needed)

Keycloak
********

1. Log into your Keycloak Admin Console
2. Select your Realm
3. Navigate to **Clients** > **Create**
4. Configure:

   * **Client ID**: Choose a meaningful name (e.g., ``django-app``)
   * **Client Protocol**: ``openid-connect``
   * **Root URL**: ``https://your-domain.com``

5. In the client settings:

   * **Access Type**: ``confidential``
   * **Valid Redirect URIs**: ``https://your-domain.com/complete/keycloak/``
   * **Web Origins**: ``https://your-domain.com``

6. **Save** and go to the **Credentials** tab to get the **Client Secret**

7. **Configure mappers** (if needed):

   * Go to **Mappers** > **Create**
   * Create an **Audience Mapper** to ensure your ``client_id`` is in the JWT's ``aud`` claim

8. **Configure algorithms** (recommended):

   * Go to **Fine Grain OpenID Connect Configuration**
   * Set **User Info Signed Response Algorithm** to ``RS256``
   * Set **Request Object Signature Algorithm** to ``RS256``

9. Get the public key:

   * Go to **Realm Settings** > **Keys** > **RS256**
   * Copy the **Public Key**

10. Provide to development team:

    * **Client ID**
    * **Client Secret**
    * **Public Key** (for RS256 signature verification)
    * **Authorization URL**: ``https://keycloak.example.com/auth/realms/your-realm/protocol/openid-connect/auth``
    * **Token URL**: ``https://keycloak.example.com/auth/realms/your-realm/protocol/openid-connect/token``

Azure Active Directory (Azure AD)
**********************************

1. Log into the Azure Portal
2. Navigate to **Azure Active Directory** > **App registrations** > **New registration**
3. Configure:

   * **Name**: Your application name
   * **Supported account types**: Choose based on your requirements
   * **Redirect URI**: Select **Web** and enter ``https://your-domain.com/complete/azuread-oauth2/``

4. After registration, note the:

   * **Application (client) ID**
   * **Directory (tenant) ID**

5. Create a **Client Secret**:

   * Go to **Certificates & secrets** > **New client secret**
   * Add a description and expiration period
   * **Copy the secret value immediately** (you won't be able to see it again)

6. Configure **API Permissions**:

   * Go to **API permissions** > **Add a permission**
   * Select **Microsoft Graph**
   * Add these delegated permissions:

     * ``User.Read``
     * ``email``
     * ``openid``
     * ``profile``

   * Click **Grant admin consent** if required

7. Provide to development team:

   * **Application (client) ID** (as ``KEY``)
   * **Client Secret** (as ``SECRET``)
   * **Tenant ID** (as ``TENANT_ID``)

Google
******

1. Go to the `Google Cloud Console`_
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth client ID**
5. Configure:

   * **Application type**: Web application
   * **Authorized JavaScript origins**: ``https://your-domain.com``
   * **Authorized redirect URIs**: ``https://your-domain.com/complete/google-oauth2/``

6. After creation, note:

   * **Client ID**
   * **Client Secret**

7. If needed, configure the **OAuth consent screen**:

   * Set application name, logo, and privacy policy
   * Add required scopes (``email``, ``profile``, ``openid``)

Common Configuration Issues
----------------------------

Redirect URI Mismatch
*********************

**Error**: "Redirect URI mismatch" or "Invalid redirect URI"

**Solution**: Ensure the redirect URI configured in your IdP **exactly matches** the URL format used by Python Social Auth, including:

* Protocol (``http://`` vs ``https://``)
* Domain name (including subdomain)
* Port number (if non-standard)
* Path (including trailing slash)

Example of correct matching::

    IdP Setting: https://app.example.com/complete/oidc/
    Application URL: https://app.example.com/complete/oidc/
    ✓ Match!

Example of incorrect matching::

    IdP Setting: https://app.example.com/complete/oidc
    Application URL: https://app.example.com/complete/oidc/
    ✗ Mismatch! (missing trailing slash)

Multiple Redirect URIs
***********************

If you need to support multiple environments (development, staging, production), configure all redirect URIs in your IdP:

* ``http://localhost:8000/complete/oidc/`` (local development)
* ``https://staging.example.com/complete/oidc/`` (staging)
* ``https://app.example.com/complete/oidc/`` (production)

HTTPS Requirement
*****************

Most IdPs require HTTPS redirect URIs in production. For local development:

* Use ``http://localhost:8000`` or ``http://127.0.0.1:8000``
* Some IdPs allow HTTP for localhost/development environments
* For proper testing, consider using a tool like ngrok to create HTTPS tunnels

Scopes and Claims
*****************

Ensure the required scopes are configured in your IdP:

**Minimum recommended scopes:**

* ``openid`` - Required for OIDC
* ``profile`` - User's basic profile (name, username)
* ``email`` - User's email address

**Optional scopes:**

* ``offline_access`` - For refresh tokens (long-lived sessions)
* ``groups`` - User's group memberships
* Custom scopes based on your application needs

Testing the Configuration
--------------------------

After configuring your IdP, test the integration:

1. **Test the Discovery Endpoint** (for OIDC)::

       curl https://your-idp-domain/.well-known/openid-configuration

   This should return a JSON document with authorization and token endpoints.

2. **Test the Authentication Flow**:

   * Navigate to your application's login page
   * Click the SSO/OIDC login button
   * You should be redirected to the IdP's login page
   * After successful login, you should be redirected back to your application

3. **Check for Common Issues**:

   * Verify the redirect URI is correctly configured
   * Ensure the client secret hasn't expired
   * Check that required scopes are granted
   * Verify user permissions and assignments in the IdP

4. **Review Application Logs**:

   Ask your development team to check the application logs for any authentication errors.

Django-Specific Configuration Notes
------------------------------------

For Django applications using ``social-auth-app-django``:

**URL Configuration**

The URLs are typically configured in your ``urls.py``::

    urlpatterns = [
        ...
        path("", include('social_django.urls', namespace="social")),
        ...
    ]

This creates the following URL patterns:

* ``/login/<backend-name>/`` - Initiates authentication
* ``/complete/<backend-name>/`` - Handles the callback (redirect URI)
* ``/disconnect/<backend-name>/`` - Disconnects the social account

**Custom Namespace**

If using a custom namespace, the redirect URI changes::

    # urls.py
    path("auth/", include('social_django.urls', namespace="social")),

The redirect URI becomes::

    https://your-domain.com/auth/complete/<backend-name>/

Security Considerations
-----------------------

1. **Use HTTPS**: Always use HTTPS in production for redirect URIs
2. **Validate State Parameter**: Python Social Auth handles this automatically
3. **Rotate Secrets**: Regularly rotate client secrets
4. **Limit Scopes**: Only request the minimum required scopes
5. **Monitor Access**: Keep logs of authentication attempts
6. **User Consent**: Ensure users understand what data is being shared
7. **Session Security**: Configure secure session cookies in your application

Additional Resources
--------------------

* :doc:`backends/oidc` - OIDC backend documentation
* :doc:`backends/okta` - Okta-specific setup
* :doc:`backends/keycloak` - Keycloak-specific setup
* :doc:`backends/azuread` - Azure AD-specific setup
* :doc:`configuration/django` - Django framework configuration
* :doc:`configuration/settings` - General settings documentation

For backend-specific details, see the :doc:`backends/index` documentation.

.. _Google Cloud Console: https://console.cloud.google.com/
