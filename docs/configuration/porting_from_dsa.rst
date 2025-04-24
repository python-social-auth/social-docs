Porting from django-social-auth
===============================


Being a derivative work from django-social-auth_, porting from it to
python-social-auth_ should be an easy task. Porting to others libraries usually
is a pain, I'm trying to make this as easy as possible.


Installed apps
--------------

On django-social-auth_ there was a single application to add into
``INSTALLED_APPS`` plus a setting to define which ORM to be used (default or
MongoEngine). Now the apps are split and there's not need for that extra
setting.

When using the default ORM::

    INSTALLED_APPS = (
        ...
        'social_django',
        ...
    )

And when using MongoEngine::

    INSTALLED_APPS = (
        ...
        'social_django_mongoengine',
        ...
    )

The models table names were defined to be compatible with those used on
django-social-auth_, so data is not needed to be migrated.


URLs
----

The URLs are namespaced, you can chose your namespace, the `example app`_ uses
the ``social`` namespace. Replace the old include with::

    urlpatterns = patterns('',
        ...
        url('', include('social_django.urls', namespace='social'))
        ...
    )

On templates use a namespaced URL::

    {% url 'social:begin' "google-oauth2" %}

Account disconnection URL would be::

    {% url 'social:disconnect_individual' provider, id %}


Porting settings
----------------

All python-social-auth_ settings are prefixed with ``SOCIAL_AUTH_``, except for
some exception on Django framework, ``AUTHENTICATION_BACKENDS`` remains the
same for obvious reasons.

All backends settings have the backend name included in the name, all uppercase
and with dashes replaced with underscores. For example, the Google OAuth2
backend is named ``google-oauth2``, so setting names related to that backend
should start with ``SOCIAL_AUTH_GOOGLE_OAUTH2_``.

Keys and secrets are some mandatory settings needed for OAuth providers; to
keep consistency the names follow the same naming convention: ``*_KEY`` for the
application key, and ``*_SECRET`` for the secret. OAuth1 backends used to have
``CONSUMER`` in the setting name but not anymore. Following with the Google
OAuth2 example::

    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '...'
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '...'

Remember that the name of the backend is needed in the settings, and names
differ a little from backend to backend; for instance the
`Facebook OAuth2 backend`_ name is ``facebook``. So the settings should be::

    SOCIAL_AUTH_FACEBOOK_KEY = '...'
    SOCIAL_AUTH_FACEBOOK_SECRET = '...'


Authentication backends
-----------------------

Import path for authentication backends changed a little, there's no more
``contrib`` module, there's no need for it. Some backends changed the names to
have some consistency. Check the backends, it should be easy to track the names
changes. Examples of the new import paths::

    AUTHENTICATION_BACKENDS = (
        'social_core.backends.open_id.OpenIdAuth',
        'social_core.backends.google.GoogleOpenId',
        'social_core.backends.google.GoogleOAuth2',
        'social_core.backends.google.GoogleOAuth',
        'social_core.backends.twitter.TwitterOAuth',
        'social_core.backends.facebook.FacebookOAuth2',
    )


Session
-------

Django stores the last authentication backend used in the user session as an
import path; this can cause import troubles when porting since the old import
paths aren't valid anymore. Some solutions to this problem are:

1. Clean the session and force the users to login again in your site

2. Run a migration script that will update the authentication backend session
   value for each session in your database. This implies figuring out the new
   import path for each backend you have configured, which is the value used in
   ``AUTHENTICATION_BACKENDS`` setting.

   `@tomgruner`_ created a Gist here_ that updates the value just for Facebook
   backend. A ``template`` for this script would look like this::

    from django.contrib.sessions.models import Session

    BACKENDS = {
        'social_auth.backends.facebook.FacebookBackend': 'social_core.backends.facebook.FacebookOAuth2'
    }

    for sess in Session.objects.iterator():
        session_dict = sess.get_decoded()

        if '_auth_user_backend' in session_dict.keys():
            # Change old backend import path from new backend import path
            if session_dict['_auth_user_backend'].startswith('social_auth'):
                session_dict['_auth_user_backend'] = BACKENDS[session_dict['_auth_user_backend']]
                new_sess = Session.objects.save(sess.session_key, session_dict, sess.expire_date)
                print 'New session saved {}'.format(new_sess.pk)


.. _django-social-auth: https://github.com/omab/django-social-auth
.. _python-social-auth: https://github.com/python-social-auth
.. _example app: https://github.com/python-social-auth/social-examples/blob/master/example-django/example/urls.py
.. _Facebook OAuth2 backend: https://github.com/python-social-auth/social-core/blob/master/social_core/backends/facebook.py#L17
.. _@tomgruner: https://github.com/tomgruner
.. _here: https://gist.github.com/tomgruner/5ce8bb1f4c55d17b5b25
