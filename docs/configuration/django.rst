Django Framework
================

Django framework has a little more support since this application was derived
from `django-social-auth`_. Here are some details on configuring this
application on Django.


Installing
----------

From pypi_::

    $ pip install social-auth-app-django

And for MongoEngine_ ORM::

    $ pip install social-auth-app-django-mongoengine

Current ``social-auth-app-django`` releases follow supported Django versions
and require Django 5.2 or newer and Python 3.10 or newer.


Quickstart
----------

This quickstart covers the essential configuration to get social authentication
working in your Django project.

**1. Add to INSTALLED_APPS**::

    INSTALLED_APPS = (
        ...
        'social_django',
    )

**2. Configure authentication backends** (example for Google OAuth2)::

    AUTHENTICATION_BACKENDS = (
        'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',  # Keep for username/password login
    )

**3. Add OAuth credentials to settings.py**:

This is where you configure your ``client_id``, ``client_secret``, and ``scope`` for each provider::

    # Google OAuth2
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'your-client-id.apps.googleusercontent.com'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'your-client-secret'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
    ]

For other providers, the pattern is ``SOCIAL_AUTH_<PROVIDER>_KEY``,
``SOCIAL_AUTH_<PROVIDER>_SECRET``, and ``SOCIAL_AUTH_<PROVIDER>_SCOPE``. See
:doc:`/backends/index` for provider-specific settings.

.. warning::
   Never commit credentials to version control. Use environment variables instead::

       import os
       SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_OAUTH2_KEY')
       SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_OAUTH2_SECRET')

**4. Add URLs to urls.py**::

    urlpatterns = [
        ...
        path('', include('social_django.urls', namespace='social')),
    ]

**5. Configure redirect URLs**::

    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

**6. Run migrations**::

    python manage.py migrate

**7. Add login form in template**::

    <form method="post" action="{% url 'social:begin' 'google-oauth2' %}">
        {% csrf_token %}
        <button type="submit">Login with Google</button>
    </form>

.. note::
   **Database considerations**: SQLite has field length limitations that can
   cause issues. For production, use PostgreSQL or MySQL. If using MySQL InnoDB
   or SQLite, add::

       SOCIAL_AUTH_UID_LENGTH = 223

For additional configuration options, see :doc:`/configuration/settings`.


Register the application
------------------------

The `Django built-in app`_ comes with two ORMs, one for default Django ORM and
another for MongoEngine_ ORM.

Add the application to ``INSTALLED_APPS`` setting, for default ORM::

    INSTALLED_APPS = (
        ...
        'social_django',
        ...
    )

And for MongoEngine_ ORM::

    INSTALLED_APPS = (
        ...
        'social_django_mongoengine',
        ...
    )

Also ensure to define the MongoEngine_ storage setting::

    SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'


Database
--------

The built-in models use Django's native ``JSONField`` to store extracted
``extra_data``.

Sync the database to create needed models once you added ``social_django`` to
your installed apps::

    ./manage.py migrate


Authentication backends
-----------------------

Add desired authentication backends to Django's AUTHENTICATION_BACKENDS_
setting::

    AUTHENTICATION_BACKENDS = (
        'social_core.backends.open_id.OpenIdAuth',
        'social_core.backends.google.GoogleOAuth2',
        'social_core.backends.twitter.TwitterOAuth',
        ...
        'django.contrib.auth.backends.ModelBackend',
    )

Take into account that backends **must** be defined in AUTHENTICATION_BACKENDS_
or Django won't pick them when trying to authenticate the user.

Don't miss ``django.contrib.auth.backends.ModelBackend`` if using ``django.contrib.auth``
application or users won't be able to login by username / password method.

For more documentation about setting backends to specific social applications,
please see the :doc:`/backends/index`.

.. _django-urls:

URLs entries
------------

Add URLs entries::

    urlpatterns = [
        ...
        path("", include('social_django.urls', namespace="social")),
        ...
    ]

In case you need a custom namespace, this setting is also needed::

    SOCIAL_AUTH_URL_NAMESPACE = 'social'

.. hint::

   In case you include the namespace from another namespace, you need to adjust
   the configuration accordingly to include the parent namespace::

      SOCIAL_AUTH_URL_NAMESPACE = 'accounts:social'


Starting Login
--------------

The ``social:begin`` view requires a ``POST`` request. Use a form and include
the CSRF token in templates that start authentication.


Templates
---------

Example of google-oauth2 backend usage in template::

    <form method="post" action="{% url 'social:begin' 'google-oauth2' %}">
        {% csrf_token %}
        <button type="submit">Google</button>
    </form>


Template Context Processors
---------------------------

There's a context processor that will add backends and associations data to
template context::

  TEMPLATES = [
      {
          ...
          'OPTIONS': {
              ...
              'context_processors': [
                  ...
                  'social_django.context_processors.backends',
                  'social_django.context_processors.login_redirect',
                  ...
              ]
          }
      }
  ]

``backends`` context processor will load a ``backends`` key in the context with
three entries on it:

``associated``
    It's a list of ``UserSocialAuth`` instances related with the currently
    logged in user. Will be empty if there's no current user.

``not_associated``
    A list of available backend names not associated with the current user yet.
    If there's no user logged in, it will be a list of all available backends.

``backends``
    A list of all available backend names.

Personalized Configuration
--------------------------

You can add (or remove) several features on the social auth pipeline.

By default there are some pipelines on social_django:

``social_details`` - Get the information we can about the user and return it in a simple
format to create the user instance later. On some cases the details are
already part of the auth response from the provider, but sometimes this
could hit a provider API.

``social_uid`` - Get the social uid from whichever service we're authing thru. The uid is
the unique identifier of the given user in the provider.

``auth_allowed`` - Verifies that the current auth process is valid within the current
project, this is where emails and domains whitelists are applied (if
defined).

``social_user`` - Checks if the current social-account is already associated in the site.

``get_username``- Make up a username for this person, appends a random string at the end if
there's any collision.

``create_user`` - Create a user account if we haven't found one yet.

``associate_user`` - Create the record that associated the social account with this user.

``extra_data`` - Populate the extra_data field in the social record with the values
specified by settings (and the default ones like access_token, etc).

``user_details`` - Update the user record with any changed info from the auth service.

Some other pipelines are available for use as well, but are not included by default:

``associate_by_email`` - Associate current auth with a user with the same email address in the DB.
Obs: This pipeline entry is not 100% secure unless you know that the providers
enabled enforce email verification on their side, otherwise a user can
attempt to take over another user account by using the same (not validated)
email address on some provider.

Usage example::

    SOCIAL_AUTH_PIPELINE = (
        'social_core.pipeline.social_auth.social_details',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.social_auth.associate_by_email',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )


ORMs
----

As detailed above the built-in Django application supports default ORM and
MongoEngine_ ORM.

When using MongoEngine_ make sure you've followed the instructions for
`MongoEngine Django integration`_, as you're now utilizing that user model. The
`MongoEngine_` backend was developed and tested with version 0.6.10 of
`MongoEngine_`.

Alternate storage models implementations currently follow a tight pattern of
models that behave near or identical to Django ORM models. It is currently
not decoupled from this pattern by any abstraction layer. If you would like
to implement your own alternate, please see the ``social_django.models`` and
``social_django_mongoengine.models`` modules for guidance.

Active users filtering
----------------------

By default the model allows only active users to authenticate. This can be
customised by ``SOCIAL_AUTH_ACTIVE_USERS_FILTER`` setting which is passed as
kwargs to the query set filter method.

.. code-block:: python
   :caption: Disable filtering for active users

   SOCIAL_AUTH_ACTIVE_USERS_FILTER = {}

.. code-block:: python
   :caption: Use custom field to filter active users

   SOCIAL_AUTH_ACTIVE_USERS_FILTER = {"deleted_account": False}



JSON field storage
------------------

The current Django models use Django's native ``models.JSONField`` for
``extra_data`` and partial pipeline data. No JSON field setting is needed for
new installations.

Older migrations still import ``social_django.fields.JSONField`` for migration
compatibility. The historical ``SOCIAL_AUTH_JSONFIELD_ENABLED``,
``SOCIAL_AUTH_JSONFIELD_CUSTOM``, and ``SOCIAL_AUTH_POSTGRES_JSONFIELD``
settings are only relevant while running those legacy migrations.


Exceptions Middleware
---------------------

A base middleware is provided that handles ``SocialAuthBaseException`` by
providing an error message to the user via configured transport mechanisms (Django
messages framework, redirect URL query parameters, or both), and then
responding with a redirect to a URL defined in one of the middleware methods.

The middleware is at ``social_django.middleware.SocialAuthExceptionMiddleware``.
Any method can be overridden, but for simplicity these two are recommended:

.. code-block:: python

    get_message(request, exception)
    get_redirect_uri(request, exception)

By default, the message is the exception message and the URL for the redirect
is the location specified by the ``LOGIN_ERROR_URL`` setting. The middleware
supports both synchronous and asynchronous Django request handlers.

If a valid backend was detected by ``strategy()`` decorator, it will be
available at ``request.strategy.backend`` and ``process_exception()`` will
use it to build a backend-dependent redirect URL but fallback to default if not
defined.

Error Transports
^^^^^^^^^^^^^^^^

In traditional server-rendered Django applications, social authentication errors
are stored in Django's flash messages framework (``django.contrib.messages``) and
rendered by server-side templates (e.g. ``{% if messages %}``).

However, in modern Single Page Applications (SPAs built with React, Vue, Angular,
etc.) or hybrid architectures, login and authentication views are handled on the
client side. When ``django.contrib.messages`` is installed (such as for the Django
Admin), error messages default to session/cookie flash storage and are never
surfaced on client-side rendered frontend login pages.

To support SPAs and hybrid setups, ``SocialAuthExceptionMiddleware`` provides a
configurable error transport mechanism via the ``SOCIAL_AUTH_ERROR_TRANSPORT``
setting.

An ``ErrorTransport`` enum is available in ``social_django.middleware``:

.. code-block:: python

    from social_django.middleware import ErrorTransport

The supported transport modes are:

``ErrorTransport.MESSAGES`` (or string ``'messages'``)
    *(Default)* Dispatches errors via ``django.contrib.messages.error`` tagged
    with ``social-auth`` and the backend name. This maintains 100% backward
    compatibility with standard Django applications.

``ErrorTransport.QUERY`` (or string ``'query'``)
    Appends the error message and backend name as URL query parameters to the
    redirect target (e.g. ``LOGIN_ERROR_URL``), allowing client-side routers
    (such as Vue Router or React Router) to inspect query parameters (e.g.,
    ``$route.query`` or ``URLSearchParams``).

Both transports can be configured together to support hybrid applications where
both Django template views and client-side SPAs handle authentication errors.

Configuration examples:

.. code-block:: python

    from social_django.middleware import ErrorTransport

    # SPA / Client-side frontend: deliver errors via URL query parameters
    SOCIAL_AUTH_ERROR_TRANSPORT = [ErrorTransport.QUERY]
    # or using string notation:
    # SOCIAL_AUTH_ERROR_TRANSPORT = 'query'

    # Hybrid application: deliver via both Django messages and URL query parameters
    SOCIAL_AUTH_ERROR_TRANSPORT = [ErrorTransport.MESSAGES, ErrorTransport.QUERY]
    # or using string notation:
    # SOCIAL_AUTH_ERROR_TRANSPORT = ['messages', 'query']

The setting accepts an ``ErrorTransport`` enum instance, a string (case-insensitive),
or an iterable (such as a list or tuple) containing enum values or strings.

Fallback behavior:

* If ``ErrorTransport.MESSAGES`` is enabled and ``django.contrib.messages`` is
  not installed or a ``MessageFailure`` occurs, the middleware automatically falls
  back to appending query parameters (unless ``ErrorTransport.QUERY`` is already active).
* If an unrecognized transport value is supplied, the middleware safely falls back
  to the default ``[ErrorTransport.MESSAGES]``.

Query Parameter Customization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When query parameter transport is active (or triggered via fallback), the redirect
destination receives two query parameters:

``message = ''``
    Message from the exception raised. In some cases, this is the error message
    returned by the provider during the authentication process.

``backend = ''``
    Backend name that was used, or ``unknown-backend`` if unresolved.

You can customize the query parameter keys globally or per-backend using Django
settings:

.. code-block:: python

    SOCIAL_AUTH_ERROR_PARAM_NAME = 'error_msg'       # Default is 'message'
    SOCIAL_AUTH_BACKEND_PARAM_NAME = 'auth_backend'  # Default is 'backend'

Alternatively, if you subclass ``SocialAuthExceptionMiddleware``, you can override
the class attributes directly:

.. code-block:: python

    class CustomExceptionMiddleware(SocialAuthExceptionMiddleware):
        ERROR_PARAM_NAME = 'error_msg'
        BACKEND_PARAM_NAME = 'auth_backend'

URL query parameters are safely merged using ``urllib.parse``: any existing query
parameters are preserved, stale error/backend parameters are updated with the
latest failure details, and URL fragments (such as ``/login/#/auth-callback``)
are preserved with query parameters placed before the hash.

Backend-specific settings
^^^^^^^^^^^^^^^^^^^^^^^^^

Error transports, error URLs, parameter names, and exception raising can all be
configured on a per-backend basis using the ``SOCIAL_AUTH_<BACKEND_NAME>_<SETTING>``
pattern.

Error transport per-backend:

.. code-block:: python

    # Default for all backends (Django messages)
    SOCIAL_AUTH_ERROR_TRANSPORT = [ErrorTransport.MESSAGES]

    # Specific to Facebook (SPA route using query parameters)
    SOCIAL_AUTH_FACEBOOK_ERROR_TRANSPORT = [ErrorTransport.QUERY]

    # Specific to Google OAuth2 (both messages and query parameters)
    SOCIAL_AUTH_GOOGLE_OAUTH2_ERROR_TRANSPORT = ['messages', 'query']

Error URLs per-backend:

.. code-block:: python

    SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'  # Default for all backends
    SOCIAL_AUTH_FACEBOOK_LOGIN_ERROR_URL = '/facebook-error/'  # Specific to Facebook
    SOCIAL_AUTH_GOOGLE_OAUTH2_LOGIN_ERROR_URL = '/google-error/'  # Specific to Google OAuth2

Query parameter names per-backend:

.. code-block:: python

    SOCIAL_AUTH_FACEBOOK_ERROR_PARAM_NAME = 'fb_error'
    SOCIAL_AUTH_FACEBOOK_BACKEND_PARAM_NAME = 'fb_backend'

Exception raising per-backend:

.. code-block:: python

    SOCIAL_AUTH_RAISE_EXCEPTIONS = False  # Default for all backends
    SOCIAL_AUTH_FACEBOOK_RAISE_EXCEPTIONS = True  # Raise exceptions only for Facebook

This is particularly useful when you want different error handling strategies for
different authentication providers, such as showing a custom error page for certain
providers or raising exceptions for debugging specific backends while keeping
others in production mode.

Exception processing is disabled if any of these settings is defined with a
``True`` value:

.. code-block:: python

    <backend name>_SOCIAL_AUTH_RAISE_EXCEPTIONS = True
    SOCIAL_AUTH_RAISE_EXCEPTIONS = True
    RAISE_EXCEPTIONS = True
    DEBUG = True


Launch Bridge Endpoints
-----------------------

When the standard ``begin`` view (``social:begin``) was made POST-only to
protect against Cross-Site Request Forgery (CSRF) vulnerabilities, workflows
that inherently rely on browser GET requests could no longer initiate
authentication without disabling CSRF protections.

Common scenarios impacted by this requirement include:

* **Identity Provider (IdP) Initiated Login**: Enterprise Single Sign-On (SSO)
  platforms (such as Okta or Microsoft Entra ID / Azure AD) that initiate
  OpenID Connect (OIDC) authentication flows by navigating the user's browser
  to an application initiation URL with an ``iss`` and ``target_link_uri``.
* **Single Page Application (SPA) & Frontend Redirects**: Frontend clients or
  same-origin apps that initiate login redirects via direct link navigation
  (``window.location.href = '/app-launch/<backend>/'``) rather than building
  and submitting an HTML form with a CSRF token.

Rather than weakening ``social:begin`` by re-allowing GET requests,
``social-app-django`` provides two dedicated, defense-in-depth bridge endpoints:

1. ``idp_launch`` (``/idp-launch/<backend>/``): Designed for external OpenID
   Connect IdP-initiated login flows.
2. ``app_launch`` (``/app-launch/<backend>/``): Designed for same-origin
   application and SPA login redirects.

Both views bridge an incoming GET redirect into an auto-submitting POST request
targeting ``social:begin`` with a valid Django CSRF token, while enforcing
strict security checks before triggering the backend authentication pipeline.

Enabling Launch Bridges
^^^^^^^^^^^^^^^^^^^^^^^

For security and backward compatibility, both launch bridge endpoints are
**opt-in** and disabled by default. When an endpoint is accessed without being
enabled, it returns an ``Http404`` (404 Not Found).

To enable one or both bridges, configure ``SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES``
in your Django ``settings.py``. The setting accepts the ``LaunchBridge`` enum
from ``social_django.utils`` or equivalent string literals:

.. code-block:: python

    from social_django.utils import LaunchBridge

    # Default (disabled) — both endpoints return 404
    SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES = None  # or []

    # Enable both bridges
    SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES = [LaunchBridge.APP, LaunchBridge.IDP]
    # Or using string literals:
    # SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES = ['app_launch', 'idp_launch']

    # Enable only App Launch (same-origin app/SPA redirects)
    SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES = [LaunchBridge.APP]
    # SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES = ['app_launch']

    # Enable only IdP Launch (external IdP-initiated OIDC login)
    SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES = [LaunchBridge.IDP]
    # SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES = ['idp_launch']

Endpoint Behaviors and Security Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both endpoints employ a layered defense model to protect users and your
application:

IdP Launch (``idp_launch``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Route: ``/idp-launch/<str:backend>/`` (URL name: ``social:idp_launch``)

Designed to handle `OIDC IdP-initiated login per the OpenID Connect Core
specification <https://openid.net/specs/openid-connect-core-1_0-36.html#ThirdPartyInitiatedLogin>`_. Enforces 8 security layers:

1. **Opt-In Gate**: Raises ``Http404`` if ``LaunchBridge.IDP`` (or
   ``'idp_launch'``) is not present in ``SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES``.
2. **Framing Protection**: Injects an ``X-Frame-Options: DENY`` header and a
   Content Security Policy (CSP) ``frame-ancestors 'none'`` directive to prevent
   clickjacking attacks.
3. **Open Redirect Prevention**: Strictly validates the ``target_link_uri``
   parameter against allowed hosts using ``is_safe_url``. Untrusted or external
   destinations are discarded to prevent open redirect vulnerabilities.
4. **Parameter Whitelisting & Issuer Validation**: Strictly accepts only
   ``iss`` and ``target_link_uri`` query parameters. Validates ``iss`` against
   the backend's configured ID token issuer(s) or alias whitelist.
5. **Authenticated Session Bypass**: If the requesting user is already
   authenticated in Django, the authentication roundtrip is skipped and the
   user is immediately redirected to the safe target destination.
6. **Fetch Metadata Validation**: Inspects ``Sec-Fetch-Dest`` and
   ``Sec-Fetch-Mode`` headers to detect suspicious framing or non-top-level
   navigation contexts.
7. **Manual Fallback**: Automatically disables JavaScript form auto-submission
   and presents the user with a manual confirmation button if framing or
   embedding is detected.
8. **CSRF Protection**: Generates and submits a POST form targeting
   ``social:begin`` with a fresh, valid Django CSRF token.

App Launch (``app_launch``)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Route: ``/app-launch/<str:backend>/`` (URL name: ``social:app_launch``)

Designed for same-origin frontend or SPA redirects. Enforces 9 security layers:

1. **Opt-In Gate**: Raises ``Http404`` if ``LaunchBridge.APP`` (or
   ``'app_launch'``) is not present in ``SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES``.
2. **Origin Validation**: Inspects ``Sec-Fetch-Site`` and requires it to be
   ``same-origin`` when present.
3. **Referer Validation**: Validates the ``Referer`` header against allowed
   hosts when present.
4. **Framing Protection**: Injects ``X-Frame-Options: DENY`` and CSP
   ``frame-ancestors 'none'`` headers.
5. **Open Redirect Prevention**: Validates the ``next`` query parameter
   against allowed hosts using ``is_safe_url``.
6. **Authenticated Session Bypass**: Immediately redirects already-authenticated
   users to the safe ``next`` destination or ``settings.LOGIN_REDIRECT_URL``.
7. **Fetch Metadata Validation**: Verifies request context using
   ``Sec-Fetch-*`` headers.
8. **Manual Fallback**: Falls back to user click confirmation if potential
   framing is detected.
9. **CSRF Protection**: Submits a POST form targeting ``social:begin`` with
   a valid Django CSRF token.

Multi-Tenant and Multiple Issuer Support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In multi-tenant OpenID Connect environments (or backends that accept multiple
issuer identifiers), valid issuers can be configured in two ways:

1. **Custom Backends**: Backends where ``id_token_issuer()`` returns a
   ``list[str]`` or ``tuple[str]``.
2. **Settings Whitelist**: The ``SOCIAL_AUTH_<BACKEND>_ALLOWED_ID_TOKEN_ISSUERS``
   setting allows specifying additional permitted issuer URLs.

For example, for a multi-tenant Okta or Entra ID backend:

.. code-block:: python

    SOCIAL_AUTH_OKTA_OAUTH2_ALLOWED_ID_TOKEN_ISSUERS = [
        'https://customer1.okta.com/oauth2/default',
        'https://customer2.okta.com/oauth2/default',
    ]

In ``app_launch``, the primary configured issuer is selected by default, or
callers can pass a specific validated issuer query parameter (e.g.
``?iss=https://customer1.okta.com/oauth2/default``).

Allowed Redirect Hosts
^^^^^^^^^^^^^^^^^^^^^^

Safe redirect URL validation for ``next`` and ``target_link_uri`` checks
the host against ``request.get_host()``, global settings, and backend-specific
settings:

.. code-block:: python

    # Global allowed hosts for redirects
    SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = ['app.example.com', 'portal.example.com']

    # Backend-specific allowed hosts
    SOCIAL_AUTH_GOOGLE_OAUTH2_ALLOWED_REDIRECT_HOSTS = ['subdomain.example.com']

Customizing the Launch Template (``launch.html``)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Both bridge views render ``social_django/launch.html``. To customize the
appearance, loading animation, or branding during the transition, create a
file named ``social_django/launch.html`` within your project's ``templates``
directory (ensuring your template loader prioritizes project templates).

Template Context Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~

The view passes the following context variables to the template:

``action_url``
    The target URL for the POST submission, which resolves to the
    ``social:begin`` view for the requested backend (e.g., ``/login/<backend>/``).

``params``
    A dictionary containing whitelisted key-value parameters to forward to
    ``social:begin`` (such as ``iss`` and ``next`` / ``target_link_uri``).
    These should be rendered as hidden input fields.

``auto_submit``
    A boolean indicating whether automatic JavaScript form submission is
    safe. When ``False`` (e.g. if the request context indicates framing), the
    template should render a manual confirmation button instead of
    auto-submitting.

``csrf_token``
    The standard Django CSRF token, required for POSTing to ``social:begin``.

Example Custom Template
~~~~~~~~~~~~~~~~~~~~~~~

Here is an example of a branded, accessible custom template:

.. code-block:: html+django

    {# templates/social_django/launch.html #}
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Authenticating...</title>
        <style>
          body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            background-color: #f8f9fa;
          }
          .card {
            background: #ffffff;
            padding: 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            max-width: 400px;
            width: 100%;
          }
          .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #0066cc;
            border-radius: 50%;
            width: 36px;
            height: 36px;
            animation: spin 1s linear infinite;
            margin: 1rem auto;
          }
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          .btn {
            background-color: #0066cc;
            color: #ffffff;
            border: none;
            padding: 0.6rem 1.2rem;
            font-size: 1rem;
            border-radius: 4px;
            cursor: pointer;
            margin-top: 1rem;
          }
          .btn:hover {
            background-color: #004c99;
          }
        </style>
      </head>
      <body>
        <div class="card">
          <form id="autoLoginForm" method="post" action="{{ action_url }}">
            {% csrf_token %}
            {% for key, value in params.items %}
              <input type="hidden" name="{{ key }}" value="{{ value }}">
            {% endfor %}

            {% if auto_submit %}
              <div class="spinner" aria-hidden="true"></div>
              <p>Signing in, please wait...</p>
              <noscript>
                <p>JavaScript is disabled in your browser.</p>
                <button type="submit" class="btn">Continue to Sign In</button>
              </noscript>
            {% else %}
              <p>Click below to continue signing in.</p>
              <button type="submit" class="btn">Sign In</button>
            {% endif %}
          </form>
        </div>

        {% if auto_submit %}
          <script>
            window.addEventListener('load', function () {
              var form = document.getElementById('autoLoginForm');
              if (form) {
                form.submit();
              }
            });
          </script>
        {% endif %}
      </body>
    </html>


Django Admin
------------

The default application (not the MongoEngine_ one) contains an ``admin.py``
module that will be auto-discovered by the usual mechanism.

But, by the nature of the application which depends on the existence of a user
model, it's easy to fall in a recursive import ordering making the application
fail to load. This happens because the admin module will build a set of fields
to populate the ``search_fields`` property to search for related users in the
administration UI, but this requires the user model to be retrieved which might
not be defined at that time.

To avoid this issue define the following setting to circumvent the import
error::

    SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['field1', 'field2']

For example::

    SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

The fields listed **must** be user models fields.

It's also possible to define more search fields, not directly related
to the user model by definig the following setting::

    SOCIAL_AUTH_ADMIN_SEARCH_FIELDS = ['field1', 'field2']

.. _MongoEngine: http://mongoengine.org
.. _MongoEngine Django integration: http://mongoengine-odm.readthedocs.org/en/latest/django.html
.. _django-social-auth: https://github.com/omab/django-social-auth
.. _Django built-in app: https://github.com/python-social-auth/social-app-django
.. _AUTHENTICATION_BACKENDS: http://docs.djangoproject.com/en/dev/ref/settings/?from=olddocs#authentication-backends
.. _django@dc43fbc: https://github.com/django/django/commit/dc43fbc2f21c12e34e309d0e8a121020391aa03a
.. _SOUTH_MIGRATION_MODULES: http://south.readthedocs.org/en/latest/settings.html#south-migration-modules
.. _pypi: http://pypi.python.org/pypi/social-auth-app-django/
