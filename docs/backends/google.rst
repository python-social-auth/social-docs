Google
======

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``google-oauth2``
     - ``social_core.backends.google.GoogleOAuth2``
   * - ``google-oauth``
     - ``social_core.backends.google.GoogleOAuth``
   * - ``google-onetap``
     - ``social_core.backends.google_onetap.GoogleOneTap``

This section describes how to setup the different services provided by Google.

Google OAuth
------------

.. attention:: **Google OAuth deprecation**
   Important: OAuth 1.0 was officially deprecated on April 20, 2012, and will be
   shut down on April 20, 2015. We encourage you to migrate to any of the other
   protocols.

Google provides ``Consumer Key`` and ``Consumer Secret`` keys to registered
applications, but also allows unregistered application to use their authorization
system with, but beware that this method will display a security banner to the
user telling that the application is not trusted.

Check `Google OAuth`_ and make your choice.

- fill ``Consumer Key`` and ``Consumer Secret`` values::

      SOCIAL_AUTH_GOOGLE_OAUTH_KEY = ''
      SOCIAL_AUTH_GOOGLE_OAUTH_SECRET = ''

anonymous values will be used if not configured as described in their
`OAuth reference`_

- setup any needed extra scope in::

      SOCIAL_AUTH_GOOGLE_OAUTH_SCOPE = [...]


Google OAuth2
-------------

Recently Google launched OAuth2 support following the definition at `OAuth2 draft`.
It works in a similar way to plain OAuth mechanism, but developers **must** register
an application and apply for a set of keys. Check `Google OAuth2`_ document for details.

IdP Setup
^^^^^^^^^

To configure Google OAuth2:

1. Go to the `Google Cloud Console <https://console.cloud.google.com/>`_
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** > **Credentials**
4. Click **Create Credentials** > **OAuth client ID**
5. Configure:

   * **Application type**: Web application
   * **Authorized redirect URIs**: ``https://your-domain.com/complete/google-oauth2/``

6. Note the **Client ID** and **Client Secret**
7. Configure the **OAuth consent screen** (``APIs & Services > OAuth consent screen``):

   * Set the **PRODUCT NAME** and other required fields
   * Add scopes: ``email``, ``profile``, ``openid``

Application Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

Fill in ``Client ID`` and ``Client Secret`` settings with values from Google::

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''

- setup any needed extra scope::

      SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [...]

Check which applications can be included in their `Google Data Protocol Directory`_

To allow user selecting Google account to use, add the ``prompt`` parameter with ``select_account`` value::

      SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {'prompt': 'select_account'}

To restrict authentication to specific domains (useful for G Suite/Google Workspace organizations), use domain whitelisting. Check the whitelists_ settings for details.


Google One Tap
---------------

`Google One Tap`_ is a bit different from the OAuth2 flow as the login process is started
on the client side. Because of this `start` url is not available, only a `complete` one.

* Additional dependencies are needed, these will be automatically installed by the ``google-onetap`` extra, for example: ``uv pip install 'social-core[google-onetap]``.
* To enable the backend create an application using the `Google
  console`_ to retrieve your `Google Client ID`.
  Make sure sure to add your website's URL to ``Authorized JavaScript origins`` and
  ``Authorized redirect URIs``
  (don't forget to also include the port number if you are using localhost).

* Fill in the key setting looking inside the Google console the subsection
  ``Credentials`` inside ``API & auth``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.google_onetap.GoogleOneTap',
    )

    SOCIAL_AUTH_GOOGLE_ONETAP_KEY = '...'
    SOCIAL_AUTH_GOOGLE_ONETAP_IGNORE_MISSING_CSRF_COOKIE = True / False

  ``SOCIAL_AUTH_GOOGLE_ONETAP_KEY`` corresponds to the variable ``CLIENT ID``.
  ``SOCIAL_AUTH_GOOGLE_ONETAP_IGNORE_MISSING_CSRF_COOKIE`` disabled the CSRF checks
  if the token is missing from the cookies. This is an optional setting
  because the cookie is not being set if authentication process started on a different
  domain (for more details check out the `related issue`_).


* Add the `One Tap snippet`_ to your page::

    <div id="g_id_onload"
        data-client_id="YOUR_GOOGLE_CLIENT_ID"
        data-login_uri="{% url 'social:complete' 'google-onetap' %}"
        data-your_own_param_1_to_login="any_value"
        data-your_own_param_2_to_login="any_value">
    </div>

* And `load the client library`_::

    <script src="https://accounts.google.com/gsi/client" async></script>



Orkut
-----

As of September 30, 2014, Orkut has been `shut down`_.

User identification
-------------------

Optional support for static and unique Google Profile ID identifiers instead of
using the e-mail address for account association can be enabled with::

      SOCIAL_AUTH_GOOGLE_OAUTH_USE_UNIQUE_USER_ID = True

or::

      SOCIAL_AUTH_GOOGLE_OAUTH2_USE_UNIQUE_USER_ID = True

depending on the backends in use.


Refresh Tokens
--------------

To get an OAuth2 refresh token along with the access token, you must pass an extra argument: ``access_type=offline``.
To do this with Google OAuth2::

      SOCIAL_AUTH_GOOGLE_OAUTH2_AUTH_EXTRA_ARGUMENTS = {
            'access_type': 'offline'
      }


.. _Google support: http://www.google.com/support/a/bin/answer.py?hl=en&answer=162105
.. _Google OAuth: http://code.google.com/apis/accounts/docs/OAuth.html
.. _Google OAuth2: http://code.google.com/apis/accounts/docs/OAuth2.html
.. _OAuth2 Registering: http://code.google.com/apis/accounts/docs/OAuth2.html#Registering
.. _OAuth2 draft: http://tools.ietf.org/html/draft-ietf-oauth-v2-10
.. _OAuth reference: http://code.google.com/apis/accounts/docs/OAuth_ref.html#SigningOAuth
.. _shut down: https://support.google.com/orkut/?csw=1#Authenticating
.. _Google Data Protocol Directory: http://code.google.com/apis/gdata/docs/directory.html
.. _whitelists: ../configuration/settings.html#whitelists
.. _Google console: https://code.google.com/apis/console
.. _Google One Tap: https://developers.google.com/identity/gsi/web/guides/features
.. _related issue: https://issuetracker.google.com/issues/226157137
.. _One Tap snippet: https://developers.google.com/identity/gsi/web/guides/display-google-one-tap
.. _load the client library: https://developers.google.com/identity/gsi/web/guides/client-library
