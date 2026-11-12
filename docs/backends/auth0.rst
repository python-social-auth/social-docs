Auth0
=====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``auth0``
     - ``social_core.backends.auth0.Auth0OAuth2``

Auth0 OAuth2
------------

Auth0 provides OAuth2 authentication. This is the original ``Auth0OAuth2`` backend.

For a newer OpenID Connect implementation, see :doc:`auth0_openidconnect`.

Setup
*****

To enable Auth0 OAuth2 support:

1. Register your application at `Auth0 Dashboard`_ to get your Auth0 domain,
   Client ID, and Client Secret.

2. Fill in the settings with your Auth0 domain, Client ID, and Client Secret::

    SOCIAL_AUTH_AUTH0_KEY = ''
    SOCIAL_AUTH_AUTH0_SECRET = ''
    SOCIAL_AUTH_AUTH0_DOMAIN = 'yourdomain.auth0.com'

   Replace ``yourdomain`` with your Auth0 tenant domain.

3. Add the backend to your authentication backends::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.auth0.Auth0OAuth2',
        ...
    )

Selecting a connection
**********************

To send users directly to a social or enterprise identity provider, pass the
Auth0 ``connection`` parameter using :ref:`auth-extra-arguments`::

    SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS = {
        'connection': 'google-oauth2',
    }

Use the connection name configured in Auth0, rather than its connection ID.
The connection must be enabled for your Auth0 application. For social and
enterprise connections, this skips the Universal Login provider selection page
and redirects to the selected identity provider. See Auth0's
`connection selection guidance`_.

To let users choose a connection when starting login, explicitly allow the
request parameter to override the configured default::

    SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS_OVERRIDE_ALLOWLIST = ['connection']

Keep ``connection`` in ``SOCIAL_AUTH_AUTH0_AUTH_EXTRA_ARGUMENTS`` as shown above.
For Django, start login with a POST form containing the CSRF token and the
selected connection::

    <form method="post" action="{% url 'social:begin' 'auth0' %}">
        {% csrf_token %}
        <input type="hidden" name="connection" value="google-oauth2">
        <button type="submit">Continue with Google</button>
    </form>

Without the override allowlist, the configured connection is used even when the
request supplies another value. The allowlist controls which parameter names
can be overridden; it does not restrict the connection values users can submit.
Connection selection controls login routing. Enforce any restrictions on which
connections a user may authenticate through in Auth0 or your application's
server-side authentication policy.

Scopes
******

You can define custom scopes using the ``SOCIAL_AUTH_AUTH0_SCOPE`` setting::

    SOCIAL_AUTH_AUTH0_SCOPE = ['openid', 'profile', 'email']

The backend will handle JWT token validation and extract user details including
username, email, full name, and profile picture.

.. _Auth0 Dashboard: https://manage.auth0.com/

.. _connection selection guidance: https://support.auth0.com/center/s/article/Authenticating-users-through-a-specific-Connection-database-social-etc
