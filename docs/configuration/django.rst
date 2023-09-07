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

When using PostgreSQL, it's recommended to use the built-in `JSONB`
field to store the extracted ``extra_data``. To enable it define the setting::

  SOCIAL_AUTH_JSONFIELD_ENABLED = True

(For Django 1.7 and higher) you need to sync the database to create needed
models once you added ``social_django`` to your installed apps::

    ./manage.py migrate


Authentication backends
-----------------------

Add desired authentication backends to Django's AUTHENTICATION_BACKENDS_
setting::

    AUTHENTICATION_BACKENDS = (
        'social_core.backends.open_id.OpenIdAuth',
        'social_core.backends.google.GoogleOpenId',
        'social_core.backends.google.GoogleOAuth2',
        'social_core.backends.google.GoogleOAuth',
        'social_core.backends.twitter.TwitterOAuth',
        'social_core.backends.yahoo.YahooOpenId',
        ...
        'django.contrib.auth.backends.ModelBackend',
    )

Take into account that backends **must** be defined in AUTHENTICATION_BACKENDS_
or Django won't pick them when trying to authenticate the user.

Don't miss ``django.contrib.auth.backends.ModelBackend`` if using ``django.contrib.auth``
application or users won't be able to login by username / password method.

Also, note that ``social_core.backends.google.GoogleOpenId`` has been deprecated.

For more documentation about setting backends to specific social applications, please see the :doc:`/backends/index`.


URLs entries
------------

Add URLs entries::

    urlpatterns = patterns('',
        ...
        url('', include('social_django.urls', namespace='social'))
        ...
    )

In case you need a custom namespace, this setting is also needed::

    SOCIAL_AUTH_URL_NAMESPACE = 'social'


Requiring POST only login
-------------------------

By default login url ``social:begin`` uses ``GET`` request if you would like to require ``POST`` only (for example to comply with SOC audits) logging in then please use::

    SOCIAL_AUTH_REQUIRE_POST = True


Templates
---------

Example of google-oauth2 backend usage in template::

    <a href="{% url "social:begin" "google-oauth2" %}">Google+</a>


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


JSON field support
------------------

Django 3.1 introduces `JSONField` support for all backends and adds a
deprecation warning.

These are the related settings to enabling this integration:

- `SOCIAL_AUTH_JSONFIELD_ENABLED` (boolean)

  Same behavior, setting name updated to match `JSONField` being supported by
  all systems::

    SOCIAL_AUTH_POSTGRES_JSONFIELD = True  # Before
    SOCIAL_AUTH_JSONFIELD_ENABLED = True  # After

- `SOCIAL_AUTH_JSONFIELD_CUSTOM` (import path)
  Allows specifying an import string. This gives better control to setting a
  custom JSONField.

  For django systems < 3.1 (technically <4), you can set the old `JSONField`
  to maintain behavior with earlier social-app-django releases::

    SOCIAL_AUTH_JSONFIELD_CUSTOM = 'django.contrib.postgres.fields.JSONField'

  For sites running or upgrading to django 3.1+, then can set this so the new
  value::

    SOCIAL_AUTH_JSONFIELD_CUSTOM = 'django.db.models.JSONField'

- Deprecating setting: `SOCIAL_AUTH_POSTGRES_JSONFIELD` (bool)
  Rename this to `SOCIAL_AUTH_JSONFIELD_ENABLED`. The setting will be deprecated
  in a future release.


Exceptions Middleware
---------------------

A base middleware is provided that handles ``SocialAuthBaseException`` by
providing a message to the user via the Django messages framework, and then
responding with a redirect to a URL defined in one of the middleware methods.

The middleware is at ``social_django.middleware.SocialAuthExceptionMiddleware``.
Any method can be overridden, but for simplicity these two are recommended::

    get_message(request, exception)
    get_redirect_uri(request, exception)

By default, the message is the exception message and the URL for the redirect
is the location specified by the ``LOGIN_ERROR_URL`` setting.

If a valid backend was detected by ``strategy()`` decorator, it will be
available at ``request.strategy.backend`` and ``process_exception()`` will
use it to build a backend-dependent redirect URL but fallback to default if not
defined.

Exception processing is disabled if any of this settings is defined with a
``True`` value::

    <backend name>_SOCIAL_AUTH_RAISE_EXCEPTIONS = True
    SOCIAL_AUTH_RAISE_EXCEPTIONS = True
    RAISE_EXCEPTIONS = True
    DEBUG = True

The redirect destination will get two ``GET`` parameters:

``message = ''``
    Message from the exception raised, in some cases it's the message returned
    by the provider during the auth process.

``backend = ''``
    Backend name that was used, if it was a valid backend.

The middleware will attempt to use the Django built-in `messages`
application to store the exception message, and tag it with
`social-auth` and the backend name. If the application is not enabled,
or a `MessageFailure` error happens, the app will default to the URL
format described above.


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
