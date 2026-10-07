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

**2. Add the exception middleware**:

Add ``SocialAuthExceptionMiddleware`` to your existing ``MIDDLEWARE`` list,
after the session, authentication, and message middleware::

    MIDDLEWARE = [
        ...
        'social_django.middleware.SocialAuthExceptionMiddleware',
    ]

This is recommended so expected authentication failures, such as an expired
login session or declined authorization, show a useful error page instead of
an HTTP 500 response. No error URL is required; configure
``SOCIAL_AUTH_LOGIN_ERROR_URL`` if you prefer a redirect to your own error page.
See :ref:`django-exception-middleware` for customization and reporting behavior.

With ``DEBUG = True``, exceptions propagate by default to aid debugging. Set
``SOCIAL_AUTH_RAISE_EXCEPTIONS = False`` to preview the error page during local
development.

**3. Configure authentication backends** (example for Google OAuth2)::

    AUTHENTICATION_BACKENDS = (
        'social_core.backends.google.GoogleOAuth2',
        'django.contrib.auth.backends.ModelBackend',  # Keep for username/password login
    )

**4. Add OAuth credentials to settings.py**:

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

**5. Add URLs to urls.py**::

    urlpatterns = [
        ...
        path('', include('social_django.urls', namespace='social')),
    ]

**6. Configure redirect URLs**::

    LOGIN_URL = '/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGOUT_REDIRECT_URL = '/'

If you need a custom authentication user model, configure it before creating
or applying your initial migrations. See :ref:`django-user-models`.

**7. Run migrations**::

    python manage.py migrate

Upgrades that add identifier-key tracking must install compatible releases of
both ``social-auth-core`` and ``social-auth-app-django`` before running this
command. The Django migration adds a blank ``id_key`` to existing social
associations; social-core then migrates those rows according to the policy in
:ref:`the configurable user ID key documentation <configurable-user-id-key>`.

**8. Add login form in template**::

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


.. _django-user-models:

User models and application data
--------------------------------

``UserSocialAuth`` stores the association between a provider account and your
Django user. It is not a separate authentication user model. By default,
``UserSocialAuth.user`` references ``settings.AUTH_USER_MODEL``, so social login
and Django's username/password login use the same user model.

Custom authentication user models
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For a new project, a simple custom user model can extend Django's
``AbstractUser``. For example, in ``accounts/models.py``::

    from django.contrib.auth.models import AbstractUser

    class User(AbstractUser):
        pass

Add ``accounts`` to ``INSTALLED_APPS`` and configure the model in
``settings.py``::

    AUTH_USER_MODEL = 'accounts.User'

Leave ``SOCIAL_AUTH_USER_MODEL`` unset: social auth uses ``AUTH_USER_MODEL``
automatically. Setting both to the same model is redundant.

``AbstractUser`` supplies the standard authentication fields and a user manager,
so this example needs no custom manager. If you change the authentication fields,
follow `Django's custom user model and manager guidance
<https://docs.djangoproject.com/en/stable/topics/auth/customizing/#specifying-a-custom-user-model>`_.
The Django storage uses ``USERNAME_FIELD`` and ``EMAIL_FIELD`` (defaulting to
``username`` and ``email``) and calls the model's default manager's
``create_user()`` method. Ensure that the arguments supplied by your pipeline
satisfy that method, including any additional required fields.

Configure a replacement user model before creating migrations or running
``migrate`` for the first time. Changing ``AUTH_USER_MODEL`` in an existing
project requires a separate schema and data migration strategy; changing the
setting alone does not migrate existing users or social associations.

.. _django-email-user:

Email-only users and custom name fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A user model does not need ``username``, ``first_name``, or ``last_name`` fields.
For example, an alternative to the simple ``AbstractUser`` subclass above can
use email for authentication and store a single ``full_name``. Define this model
and its manager in ``accounts/models.py``::

    from django.contrib.auth.base_user import BaseUserManager
    from django.contrib.auth.models import AbstractUser
    from django.db import models

    class UserManager(BaseUserManager):
        def create_user(self, email, password=None, **extra_fields):
            if not email:
                raise ValueError('An email address is required')
            user = self.model(email=self.normalize_email(email), **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user

        def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault('is_staff', True)
            extra_fields.setdefault('is_superuser', True)
            if not extra_fields['is_staff'] or not extra_fields['is_superuser']:
                raise ValueError('A superuser must have is_staff and is_superuser set')
            return self.create_user(email, password, **extra_fields)

    class User(AbstractUser):
        username = None
        first_name = None
        last_name = None
        email = models.EmailField(unique=True)
        full_name = models.CharField(max_length=255, blank=True)

        USERNAME_FIELD = 'email'
        EMAIL_FIELD = 'email'
        REQUIRED_FIELDS = []
        objects = UserManager()

        def get_full_name(self):
            return self.full_name

        def get_short_name(self):
            return self.full_name

Configure social auth to create users using email and update their custom name
field in ``settings.py``::

    AUTH_USER_MODEL = 'accounts.User'
    SOCIAL_AUTH_USER_FIELDS = ['email']
    SOCIAL_AUTH_USER_FIELD_MAPPING = {'fullname': 'full_name'}

``SOCIAL_AUTH_USER_FIELDS`` controls the arguments passed by the default
``create_user`` pipeline step. Omitting ``username`` also makes ``get_username``
skip username generation. Use the prefixed setting, rather than ``USER_FIELDS``.
The provider must supply an email, or your pipeline must obtain one before
``create_user`` runs.

Providers use the normalized detail key ``fullname``, while this model uses
``full_name``. ``SOCIAL_AUTH_USER_FIELD_MAPPING`` applies that mapping during
``user_details``, after user creation; it does not rename arguments to
``create_user``. The example therefore allows a blank name initially. If your
manager requires a name at creation, add a step before ``create_user`` that
returns ``{'full_name': details.get('fullname') or ''}`` and include
``full_name`` in ``SOCIAL_AUTH_USER_FIELDS``. Obtain or validate any required
name in that step instead of relying on an empty default.

Keep ``social_names`` in the pipeline to normalize provider names, and
``user_details`` to apply the mapping. Details for missing model attributes,
such as ``first_name``, are skipped. Adapt Django's admin fieldsets and user
forms to the fields on this model; the default configurations reference the
removed fields.

Storing application data
^^^^^^^^^^^^^^^^^^^^^^^^

For information unrelated to authentication, use ordinary related models.
A profile stores one record per user, while a foreign key can store many user
actions. For example, in ``accounts/models.py``::

    from django.conf import settings
    from django.db import models

    class Profile(models.Model):
        user = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            related_name='profile',
        )
        biography = models.TextField(blank=True)

    class UserAction(models.Model):
        user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        name = models.CharField(max_length=100)
        created = models.DateTimeField(auto_now_add=True)

Profiles are not created automatically. Your application can initialize them
when needed::

    from accounts.models import Profile, UserAction

    profile, created = Profile.objects.get_or_create(user=request.user)
    UserAction.objects.create(user=request.user, name='completed_tutorial')

No custom authentication pipeline is needed to save data from ordinary site
actions. Add a pipeline step only when you want to initialize or populate a
profile during login; see :ref:`django-profile-pipeline`.

All apps in the same project can use these relationships. Use
``settings.AUTH_USER_MODEL`` in model relationships and ``get_user_model()``
when you need the user class at runtime::

    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.get(pk=user_id)

See `Django's authentication customization documentation
<https://docs.djangoproject.com/en/stable/topics/auth/customizing/>`_ for profile
models, custom users, managers, and admin integration.

Admin and social login
^^^^^^^^^^^^^^^^^^^^^^

Use the same authentication model for admin and social login, with
``is_staff`` and permissions controlling admin access. Keep application data
in related models as shown above.

``SOCIAL_AUTH_USER_MODEL`` overrides the social-account foreign key; it does
not create independent authentication sessions. Django's standard authentication
session represents one logged-in user at a time.

If ``SOCIAL_AUTH_USER_MODEL`` targets a different model from ``AUTH_USER_MODEL``,
an admin user supplied as ``request.user`` can cause
``ValueError: Cannot query "...": Must be "..." instance.`` For example, the
social-auth context processor queries associations for ``request.user`` and
Django rejects a user instance that does not match the foreign key's model.
An override alone therefore does not provide two independent authentication
systems with simultaneous admin and social logins.


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

.. _django-custom-login:

Logging in users from custom views
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When multiple authentication backends are configured, Django's
``django.contrib.auth.login()`` needs to know which backend to store in the
session. Pass its dotted import path as the ``backend`` argument, or use a user
instance whose ``backend`` attribute was set by ``authenticate()``. This attribute
is not a model field: a user created directly or loaded again from the database
does not automatically have it.

For example, a custom account activation view using ``ModelBackend`` can log in
the user after validating the activation token and activating the account::

    from django.contrib.auth import login

    # Validate the activation token and activate the account before this call.
    login(request, user, backend='django.contrib.auth.backends.ModelBackend')

Use the backend appropriate for your authentication flow, and ensure it is listed
in ``AUTHENTICATION_BACKENDS``. Adding a ``backend`` parameter to your own view's
signature only helps if you pass it to ``login()``.

Without an explicit backend or ``user.backend``, Django raises ``ValueError``
when more than one backend is configured, with the message
``You have multiple authentication backends configured and therefore must provide
the `backend` argument or set the `backend` attribute on the user.``

``django.contrib.auth.authenticate()`` has a different purpose: it checks
credentials against the configured backends. For username/password login, use::

    from django.contrib.auth import authenticate, login

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)

Do not pass a dotted import path as ``backend`` to ``authenticate()`` to select a
backend. Its keyword arguments are forwarded to the authentication backends;
social auth backends expect a backend instance for that argument. Passing a
string can cause ``AttributeError: 'str' object has no attribute 'name'``.

The standard ``social:complete`` view selects the social backend automatically
before calling ``login()``, including when resuming an email validation pipeline.
For details about Django's backend selection, see `Selecting the authentication
backend <https://docs.djangoproject.com/en/stable/topics/auth/default/#selecting-the-authentication-backend>`_.

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
four entries on it:

``associated``
    It's a list of ``UserSocialAuth`` instances related with the currently
    logged in user. Will be empty if there's no current user.

``not_associated``
    A list of available backend names not associated with the current user yet.
    If there's no user logged in, it will be a list of all available backends.

``backends``
    A list of all available backend names.

``metadata``
    A dictionary of display titles and optional static icon paths, keyed by
    backend identifier.

Backend display names and icons
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Backend classes expose ``title`` (a human-readable sign-in label) and ``icon``
(an optional bundled SVG filename). Their ``name`` remains the stable identifier
used in routes, settings, and stored associations. Custom backends may override
these attributes; absent titles fall back to ``name`` and absent icons to ``None``.

Register the icon finder after Django's standard finders::

    STATICFILES_FINDERS = [
        "django.contrib.staticfiles.finders.FileSystemFinder",
        "django.contrib.staticfiles.finders.AppDirectoriesFinder",
        "social_django.finders.SocialAuthIconFinder",
    ]

Run ``collectstatic`` after installing or upgrading. Applications can override
bundled assets by supplying the same ``social_auth/icons/<filename>`` path.
Only provider logos are bundled. They retain their respective owners' rights
and branding terms; they are not relicensed under the Python library's BSD
license. See the packaged icon provenance notice for official artwork sources and
branding references. Applications supply their own generic or fallback icons.

The existing context processor adds ``backends.metadata``, a dictionary keyed
by backend identifier. Each value contains ``title`` and ``icon``; ``icon`` is a
static path or ``None``, not a URL. For example::

    {% load static %}
    {% for name, provider in backends.metadata.items %}
      <form method="post" action="{% url 'social:begin' name %}">
        {% csrf_token %}
        <button type="submit">
          {% if provider.icon %}
            <img src="{% static provider.icon %}" alt="" aria-hidden="true">
          {% endif %}
          {{ provider.title }}
        </button>
      </form>
    {% endfor %}

Existing backend and association lists retain their original formats.

Personalized Configuration
--------------------------

You can add (or remove) several features on the social auth pipeline.

By default there are some pipelines on social_django:

``social_details`` - Get the information we can about the user and return it in a simple
format to create the user instance later. On some cases the details are
already part of the auth response from the provider, but sometimes this
could hit a provider API.

``social_names`` - Fill missing name representations; see :ref:`name-normalization`.

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
        'social_core.pipeline.social_auth.social_names',
        'social_core.pipeline.social_auth.social_uid',
        'social_core.pipeline.social_auth.social_user',
        'social_core.pipeline.user.get_username',
        'social_core.pipeline.social_auth.associate_by_email',
        'social_core.pipeline.user.create_user',
        'social_core.pipeline.social_auth.associate_user',
        'social_core.pipeline.social_auth.load_extra_data',
        'social_core.pipeline.user.user_details',
    )


.. _django-link-social-accounts:

Linking multiple social accounts to one user
--------------------------------------------------

One Django user can have multiple ``UserSocialAuth`` associations, including
multiple accounts from the same provider. Each provider account can belong to
only one local user; trying to link an account already owned by another user
raises an association error.

To link an additional account, log in to the target local user first, then
start the normal social-auth flow from an account settings page. For example,
show this form only to authenticated users::

    <form method="post" action="{% url 'social:begin' 'google-oauth2' %}">
        {% csrf_token %}
        <button type="submit">Link a Google account</button>
    </form>

Select the additional account at the provider and complete authentication while
remaining logged in locally. The standard Django views pass ``request.user``
to the pipeline, and ``associate_user`` links the provider account to that user
instead of creating a new local user. If the provider automatically selects an
already linked account, use its account-selection controls to choose the other
account. Once linked, a later login with either provider account resolves to
the same local user. Custom login views must also pass the authenticated user
to the authentication flow to preserve this linking behavior.

``associate_by_email`` is optional and disabled by default. It finds an existing
local user with the same email returned by the provider when no user has
already been selected. It does not group different Gmail addresses into a
shared Customer Support account. Enable it only for providers whose returned
email ownership you can trust; see the verification constraints in the
pipeline guidance above.

For staff sharing a local support account, explicitly link each authorized
provider account as above, or implement a pipeline step with an application
policy that selects the permitted target user. Place such a step after
``social_user`` and before ``create_user`` and ``associate_user``; return the
selected ``user`` only after validating authorization and any existing
association. Do not select a shared user solely because someone supplies an
email address or uses Gmail. Separate staff users with shared permissions are
an alternative when you need actions attributed to individual staff members.

Linking runs the normal pipeline, including user-detail updates. If a shared
account's name should remain unchanged, protect the model field, for example
``SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['full_name']`` for the email-only model
above.


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


.. _django-exception-middleware:

Exceptions Middleware
---------------------

A base middleware handles ``SocialAuthBaseException`` by redirecting to a
configured error URL or rendering an error page. It supports both synchronous
and asynchronous Django request handlers. Add it to ``MIDDLEWARE``, after your
session, authentication, and message middleware:

.. code-block:: python

    MIDDLEWARE = [
        # ...
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'social_django.middleware.SocialAuthExceptionMiddleware',
    ]

To redirect failures to an application error page, configure:

.. code-block:: python

    SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
    SOCIAL_AUTH_RAISE_EXCEPTIONS = False

The redirect uses the configured error transports described below. The default
message is the safe exception message. A backend attached by the ``psa()``
decorator is available at ``request.backend``; backend-specific settings take
precedence over global settings.

Without this middleware, Social Auth exceptions are left to Django's exception
handling and can produce an HTTP 500 response.

Fallback error page
^^^^^^^^^^^^^^^^^^^

When ``SOCIAL_AUTH_LOGIN_ERROR_URL`` is unset, ``None``, or an empty string, the
middleware renders ``social_django/error.html`` directly. It does not use flash
messages or query parameters, so the page works even when session cookies are
unavailable. Explicit exception propagation still takes precedence, as described
under exception raising below.

The response status depends on the failure:

.. list-table::
   :header-rows: 1

   * - Exception family or reason
     - HTTP status
   * - ``AuthInputError``
     - 400
   * - ``AuthSessionError``, ``AuthCredentialError``, ``AuthPolicyError``, ``AuthCanceled``
     - 403
   * - ``AuthAssociationError``
     - 409
   * - ``AuthResponseError``
     - 502
   * - ``AuthProviderError``: connection, unavailability, rate limit, or custom codes
     - 503
   * - ``AuthProviderError``: ``timeout``
     - 504
   * - ``AuthProviderError``: ``tls_error`` or ``http_error``
     - 502
   * - Configuration errors, unknown errors, or other base exceptions
     - 500

The reason codes ``response_expired`` and ``nonce_mismatch`` override the family
status with 403; ``invalid_expiry`` overrides it with 500. Other custom codes
inherit the family's status. Provider HTTP statuses are not forwarded directly.

The bundled page shows the safe message and guidance selected from the suggested
recovery action. Only ``session_context_missing`` adds a hint about session expiry,
cookies, and restarting login in the same browser and container. These are possible
causes, not a diagnosis. The page does not automatically retry authentication.

Override ``social_django/error.html`` in your application's templates to customize
its presentation. The middleware supplies ``message``, ``error_code``,
``error_source``, ``error_stage``, and ``error_recovery``; it does not supply the raw
exception, provider diagnostics, or identifying context. Normal Django template
context processors still apply. The response includes headers preventing caching.

You can also subclass the middleware and replace its ``MIDDLEWARE`` entry with
your subclass. The following methods accept ``request`` and ``exception``:

* ``get_message()`` customizes the message for redirects and rendered pages.
* ``get_redirect_uri()`` selects the error redirect URL.
* ``get_error_status()`` selects the rendered response's HTTP status.
* ``render_error()`` customizes the rendered response and its reporting.

For example, an application can change the status used for explicit cancellation:

.. code-block:: python

    from social_core.exceptions import AuthCanceled
    from social_django.middleware import SocialAuthExceptionMiddleware

    class CustomExceptionMiddleware(SocialAuthExceptionMiddleware):
        def get_error_status(self, request, exception):
            if isinstance(exception, AuthCanceled):
                return 400
            return super().get_error_status(request, exception)

Rendered 4xx failures are logged at warning level using safe classification
fields, without tracebacks. Rendered 5xx failures are logged at error level with
the original exception and traceback so server-side defects remain diagnosable.
Tracebacks are included only in server logs, not in the rendered page.
Rendering a 500 handles the exception instead of propagating it, so
exception-based monitoring may no longer receive it. Configure monitoring for
the logs or override ``render_error()`` to integrate your reporting. Unrelated
exceptions still propagate through Django normally.

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
    Safe default message from the exception raised. Provider descriptions are
    retained in the exception's diagnostic ``detail`` and are not sent to clients.

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

Exception processing is disabled when the effective ``RAISE_EXCEPTIONS``
setting is true. Settings are checked in this order, and the first configured
value wins:

1. ``SOCIAL_AUTH_<BACKEND>_RAISE_EXCEPTIONS`` (uppercase backend name, with
   hyphens replaced by underscores).
2. ``SOCIAL_AUTH_RAISE_EXCEPTIONS``.
3. ``RAISE_EXCEPTIONS``.
4. ``DEBUG`` as the default when none of these settings is configured.

For example, ``SOCIAL_AUTH_RAISE_EXCEPTIONS = False`` enables handling even with
``DEBUG = True``; a backend-specific true value overrides that global false value.


Structured authentication errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`authentication-exceptions` for the exception families and recovery
contract. The middleware uses safe default messages; provider diagnostics and
identifying context are not included in client transports.

Enable metadata in query transport (including message-storage fallback) with:

.. code-block:: python

    SOCIAL_AUTH_ERROR_INCLUDE_METADATA = True  # Default: False

The redirect receives ``error_code``, ``error_source``, ``error_stage``, and
``error_recovery`` alongside the configured message/backend parameters.
Backend-specific settings are supported. Existing query parameters and fragments
are preserved; stale metadata values are replaced when metadata is enabled.
If a configured message/backend parameter name matches a metadata key, the
configured parameter takes precedence and that metadata field is omitted.

Applications should select their own messages and redirects from stable codes,
and should decide reporting independently of suggested recovery actions.
Subclasses overriding ``dispatch_error`` or ``append_query_params`` must accept
the new optional ``metadata`` argument.


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
   application and SPA login redirects with OpenID Connect backends.

Both views bridge an incoming GET redirect into an auto-submitting POST request
targeting ``social:begin`` with a valid Django CSRF token, while enforcing
strict security checks before triggering the backend authentication pipeline.

.. note::

   **OpenID Connect (OIDC) Backend Prerequisite**: Both ``idp_launch`` and
   ``app_launch`` strictly require an OpenID Connect backend (or a custom backend
   that provides a valid, RFC-compliant HTTPS ID token issuer via
   ``backend.id_token_issuer()`` or the ``SOCIAL_AUTH_<BACKEND>_ID_TOKEN_ISSUER``
   setting).

   If either endpoint is accessed with a backend that does not support ID token
   issuer validation (such as non-OIDC OAuth 1.0 or OAuth 2.0 backends like Facebook,
   GitHub, or Twitter), or if the backend does not supply a valid HTTPS issuer URL,
   the launch bridge immediately rejects the request with HTTP 400 (``BadRequest``).


Enabling Launch Bridges
^^^^^^^^^^^^^^^^^^^^^^^

For security and backward compatibility, both launch bridge endpoints are
**opt-in** and disabled by default. When an endpoint is accessed without being
enabled, it returns an ``Http404`` (404 Not Found).

To enable one or both bridges, configure ``SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES``
in your Django ``settings.py``. The setting accepts the ``LaunchBridge`` enum
from ``social_django.constants`` or equivalent string literals:

.. code-block:: python

    from social_django.constants import LaunchBridge

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
   the backend's configured ID token issuer(s) or alias whitelist. Requires a
   valid RFC-compliant HTTPS issuer; backends without issuer support reject
   requests with HTTP 400 (``BadRequest``).
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

Designed for same-origin frontend or SPA redirects with OpenID Connect (OIDC) backends. Enforces 10 security layers:

1. **Opt-In Gate**: Raises ``Http404`` if ``LaunchBridge.APP`` (or
   ``'app_launch'``) is not present in ``SOCIAL_AUTH_ENABLE_LAUNCH_BRIDGES``.
2. **Backend Issuer Validation**: Requires the backend to provide a valid,
   RFC-compliant HTTPS ID token issuer (via ``id_token_issuer()`` or
   ``SOCIAL_AUTH_<BACKEND>_ID_TOKEN_ISSUER``). Non-OIDC backends (such as
   Facebook or GitHub) or backends with non-HTTPS issuers immediately raise
   HTTP 400 (``BadRequest``). If an optional ``iss`` query parameter is
   provided, it is validated against the backend's allowed issuers.
3. **Origin Validation**: Inspects ``Sec-Fetch-Site`` and requires it to be
   ``same-origin`` when present.
4. **Referer Validation**: Validates the ``Referer`` header against allowed
   hosts when present.
5. **Framing Protection**: Injects ``X-Frame-Options: DENY`` and CSP
   ``frame-ancestors 'none'`` headers.
6. **Open Redirect Prevention**: Validates the ``next`` query parameter
   against allowed hosts using ``is_safe_url``.
7. **Authenticated Session Bypass**: Immediately redirects already-authenticated
   users to the safe ``next`` destination or ``settings.LOGIN_REDIRECT_URL``.
8. **Fetch Metadata Validation**: Verifies request context using
   ``Sec-Fetch-*`` headers.
9. **Manual Fallback**: Falls back to user click confirmation if potential
   framing is detected.
10. **CSRF Protection**: Submits a POST form targeting ``social:begin`` with
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
``?iss=https://customer1.okta.com/oauth2/default``). If the requested backend
does not configure an issuer or if an unapproved ``iss`` parameter is supplied,
the view returns HTTP 400 (``BadRequest``).

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


Authentication storage cleanup
------------------------------

Schedule ``manage.py clearsocial`` regularly, for example hourly. It removes
unused verification codes and partial pipelines older than ``--age`` days
(default: 14), and expired OpenID associations and OpenID Connect nonces.
Association expiry uses each record's ``issued`` timestamp and ``lifetime``;
``--age`` does not change this policy. Active associations and linked user
accounts are preserved.

Applications with their own scheduled tasks can call
``social_django.models.Association.cleanup_expired()`` directly. Expiry is
checked during OIDC login validation even when scheduled cleanup has not run.

When upgrading to nonce lifetime enforcement, stop old login-serving processes,
apply the social-auth-app-django migrations, and start processes with the
coordinated social-auth-core and social-auth-app-django versions. The migration
gives existing OIDC nonce records with an empty secret, ``issued=0``, and
``lifetime=0`` a 30-minute grace period. After that period, validation rejects
them and the next cleanup removes them. Other storage integrations need their
own equivalent upgrade conversion; see :doc:`/storage`.
