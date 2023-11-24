Configuration
=============

Application setup
-----------------

Once the application is installed (check Installation_) define the following
settings to enable the application behavior. Also check the sections dedicated
to each framework for detailed instructions.


Settings name
-------------

Almost all settings are prefixed with ``SOCIAL_AUTH_``, there are some
exceptions for Django framework like ``AUTHENTICATION_BACKENDS``.

All settings can be defined per-backend by adding the backend name to the
setting name, like ``SOCIAL_AUTH_TWITTER_LOGIN_URL``. Settings discovery is done
by reducing the name starting with the backend setting, then the app setting,
and finally the global setting, for example::

    SOCIAL_AUTH_TWITTER_LOGIN_URL
    SOCIAL_AUTH_LOGIN_URL
    LOGIN_URL

The backend name is generated from the ``name`` attribute from the backend
class by uppercasing it and replacing ``-`` with ``_``.


Keys and secrets
----------------

- Set up needed OAuth keys (see OAuth_ section for details)::

    SOCIAL_AUTH_TWITTER_KEY = 'foobar'
    SOCIAL_AUTH_TWITTER_SECRET = 'bazqux'

OpenID backends don't require keys usually, but some need some API Key to
call any API on the provider. Check Backends_ sections for details.


Authentication backends
-----------------------

Register the backends you plan to use, on Django framework use the usual
``AUTHENTICATION_BACKENDS`` settings, for others, define
``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        'social_core.backends.open_id.OpenIdAuth',
        'social_core.backends.google.GoogleOpenId',
        'social_core.backends.google.GoogleOAuth2',
        'social_core.backends.google.GoogleOAuth',
        'social_core.backends.twitter.TwitterOAuth',
        'social_core.backends.yahoo.YahooOpenId',
        ...
    )


URLs options
------------

These URLs are used on different steps of the auth process, some for successful
results and others for error situations.

``SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/logged-in/'``
    Used to redirect the user once the auth process ended successfully. The
    value of ``?next=/foo`` is used if it was present

``SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'``
    URL where the user will be redirected in case of an error

``SOCIAL_AUTH_LOGIN_URL = '/login-url/'``
    Is used as a fallback for ``LOGIN_ERROR_URL``

``SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/new-users-redirect-url/'``
    Used to redirect new registered users, will be used in place of
    ``SOCIAL_AUTH_LOGIN_REDIRECT_URL`` if defined. Note that ``?next=/foo`` is appended if present,
    if you want new users to go to next, you'll need to do it yourself.

``SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/new-association-redirect-url/'``
    Like ``SOCIAL_AUTH_NEW_USER_REDIRECT_URL`` but for new associated accounts
    (user is already logged in). Used in place of ``SOCIAL_AUTH_LOGIN_REDIRECT_URL``

``SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = '/account-disconnected-redirect-url/'``
    The user will be redirected to this URL when a social account is
    disconnected

``SOCIAL_AUTH_INACTIVE_USER_URL = '/inactive-user/'``
    Inactive users can be redirected to this URL when trying to authenticate.

Successful URLs will default to ``SOCIAL_AUTH_LOGIN_URL`` while error URLs will
fallback to ``SOCIAL_AUTH_LOGIN_ERROR_URL``.


User model
----------

``UserSocialAuth`` instances keep a reference to the ``User`` model of your
project, since this is not known, the ``User`` model must be configured by
a setting::

    SOCIAL_AUTH_USER_MODEL = 'foo.bar.User'

``User`` model must have a ``username`` and ``email`` field, these are
required.

Also an ``is_authenticated`` and ``is_active`` boolean flags are recommended,
these can be methods if necessary (must return ``True`` or ``False``). If the
model lacks them a ``True`` value is assumed.


Tweaking some fields length
---------------------------

Some databases impose limitations on index columns (like MySQL InnoDB). These
limitations won't play nice on some ``UserSocialAuth`` fields. To avoid such
errors, define some of the following settings.

``SOCIAL_AUTH_UID_LENGTH = <int>``
    Used to define the max length of the field `uid`. A value of 223 should work
    when using MySQL InnoDB which impose a 767 bytes limit (assuming UTF-8
    encoding).

``SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = <int>``
    ``Nonce`` model has a unique constraint over ``('server_url', 'timestamp',
    'salt')``, salt has a max length of 40, so ``server_url`` length must be
    tweaked using this setting.

``SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = <int>`` or ``SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = <int>``
    ``Association`` model has a unique constraint over ``('server_url',
    'handle')``, both fields lengths can be tweaked by these settings.


Username generation
-------------------

Some providers return a username, others just an ID or email or first and last
names. The application tries to build a meaningful username when possible but
defaults to generating one if needed.

A UUID is appended to usernames in case of collisions. Here are some settings
to control username generation.

``SOCIAL_AUTH_UUID_LENGTH = 16``
    This controls the length of the UUID appended to usernames.

``SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True``
    If you want to use the full email address as the ``username``, define this
    setting.

``SOCIAL_AUTH_SLUGIFY_USERNAMES = False``
    For those that prefer slugged usernames, the ``get_username`` pipeline can
    apply a slug transformation (code borrowed from Django project) by defining
    this setting to ``True``. The feature is disabled by default to not
    force this option to all projects.

``SOCIAL_AUTH_CLEAN_USERNAMES = True``
    By default `a set of regular expressions`_ are applied over
    usernames to clean them from usual undesired characters like
    spaces. Set this setting to ``False`` to disable this behavior.

``SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = None``
    Sometimes extra cleaning up of usernames is needed in order to fit
    properly in a project, this setting is used to point to a function
    that will be called with the current username value, the output
    will be used as the new username. This method can be called
    multiple times in case of a collision. The setting value must be
    in the format of an import path.


Extra arguments on auth processes
---------------------------------

Some providers accept particular GET parameters that produce different results
during the auth process, usually used to show different dialog types (mobile
version, etc).

You can send extra parameters on auth process by defining settings per backend,
example to request Facebook to show Mobile authorization page, define::

      SOCIAL_AUTH_FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'display': 'touch'}

For other providers, just define settings in the form::

      SOCIAL_AUTH_<uppercase backend name>_AUTH_EXTRA_ARGUMENTS = {...}

Also, you can send extra parameters on request token process by defining
settings in the same way explained above but with this other suffix::

      SOCIAL_AUTH_<uppercase backend name>_REQUEST_TOKEN_EXTRA_ARGUMENTS = {...}

Basic information is requested to the different providers in order to create
a coherent user instance (with first and last name, email and full name), this
could be too intrusive for some sites that want to ask users the minimum data
possible. It's possible to override the default values requested by defining
any of the following settings, for Open Id providers::

    SOCIAL_AUTH_<BACKEND_NAME>_IGNORE_DEFAULT_AX_ATTRS = True
    SOCIAL_AUTH_<BACKEND_NAME>_AX_SCHEMA_ATTRS = [
        (schema, alias)
    ]

For OAuth backends::

    SOCIAL_AUTH_<BACKEND_NAME>_IGNORE_DEFAULT_SCOPE = True
    SOCIAL_AUTH_<BACKEND_NAME>_SCOPE = [
        ...
    ]


Processing requests and redirects
---------------------------------

The application issues several redirects and API calls. The following settings
allow some tweaks to the behavior of these.

``SOCIAL_AUTH_SANITIZE_REDIRECTS = False``
    The auth process finishes with a redirect, by default it's done to the
    value of ``SOCIAL_AUTH_LOGIN_REDIRECT_URL`` but can be overridden with
    ``next`` GET argument. If this setting is ``True``, this application will
    vary the domain of the final URL and only redirect to it if it's on the
    same domain.
    
``SOCIAL_AUTH_ALLOWED_REDIRECT_HOSTS = ['foo', 'bar']``
    To allow redirection to certain domains while keeping the more restrictive
    ``SOCIAL_AUTH_SANITIZE_REDIRECTS = True`` setting. This will redirect to the
    ``next`` GET argument if the hostname is on the list, otherwise it defaults
    to the value of ``SOCIAL_AUTH_LOGIN_REDIRECT_URL``.

``SOCIAL_AUTH_REDIRECT_IS_HTTPS = False``
    On projects behind a reverse proxy that uses HTTPS, the redirect URIs
    can have the wrong schema (``http://`` instead of ``https://``) if
    the request lacks the appropriate headers, which might cause errors during
    the auth process. To force HTTPS in the final URIs set this setting to
    ``True``

``SOCIAL_AUTH_REQUESTS_TIMEOUT = 10``
    Any ``requests.request`` call will be performed with the default timeout
    value, to change it without affecting the global socket timeout define this
    setting (the value specifies timeout seconds).

``SOCIAL_AUTH_URLOPEN_TIMEOUT``
    Deprecated: this was the old timeout setting before the move to ``requests``
    If it's defined, it will be used as the fallback for the above setting.
    If the above setting is defined, this one will be ignored.

``SOCIAL_AUTH_VERIFY_SSL``
    If set, it will be passed as the ``verify`` parameter to ``requests.request``
    calls. To learn more, check the `Requests' SSL verification page`_.

``SOCIAL_AUTH_PROXIES``
    If set, it will be passed as the ``proxies`` parameter to ``requests.request``
    calls. To learn more, check the `Requests' Proxies page`_.

Whitelists
----------

Registration can be limited to a set of users identified by their email
address or domain name. To white-list just set any of these settings:

``SOCIAL_AUTH_<BACKEND_NAME>_WHITELISTED_DOMAINS = ['foo.com', 'bar.com']``
    Supply a list of domain names to be white-listed. Any user with an email
    address on any of the allowed domains will login successfully, otherwise
    ``AuthForbidden`` is raised.

``SOCIAL_AUTH_<BACKEND_NAME>_WHITELISTED_EMAILS = ['me@foo.com', 'you@bar.com']``
    Supply a list of email addresses to be white-listed. Any user with an email
    address in this list will login successfully, otherwise ``AuthForbidden``
    is raised.


Miscellaneous settings
----------------------

``SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email',]``
    During the pipeline process a ``dict`` named ``details`` will be populated
    with the needed values to create the user instance, but it's also used to
    update the user instance. Any value in it will be checked as an attribute
    in the user instance (first by doing ``hasattr(user, name)``). Usually
    there are attributes that cannot be updated (like ``username``, ``id``,
    ``email``, etc.), those fields need to be *protect*. Set any field name that
    requires *protection* in this setting, and it won't be updated.


``SOCIAL_AUTH_IMMUTABLE_USER_FIELDS = ['email',]``
    Set any field name that requires *protection* in this setting, and it won't
    be updated after inital population. This setting is similar to 
    ``SOCIAL_AUTH_PROTECTED_USER_FIELDS`` in that they both do not allow changes 
    of the data - however this one allows it to be set if no prior value exists.
    An example use case might be an application that seeds data from a social 
    plaform but allows the users to override it locally.    


``SOCIAL_AUTH_SESSION_EXPIRATION = False``
    By default, user session expiration time will be set by your web
    framework (in Django, for example, it is set with
    `SESSION_COOKIE_AGE`_). Some providers return the time that the
    access token will live, which is stored in ``UserSocialAuth.extra_data``
    under the key ``expires``. Changing this setting to True will override your
    web framework's session length setting and set user session lengths to
    match the ``expires`` value from the auth provider.

``SOCIAL_AUTH_OPENID_PAPE_MAX_AUTH_AGE = <int value>``
    Enable `OpenID PAPE`_ extension support by defining this setting.

``SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['foo',]``
    If you want to store extra parameters from POST or GET in session, like it
    was made for ``next`` parameter, define this setting with the parameter
    names.

    In this case ``foo`` field's value will be stored when user follows this
    link ``<a href="{% url socialauth_begin 'github' %}?foo=bar">...</a>``.

``SOCIAL_AUTH_PASSWORDLESS = False``
    When this setting is ``True`` and ``social_core.pipeline.mail.send_validation``
    is enabled, it allows the implementation of a `passwordless authentication
    mechanism`_. Example of this implementation can be found at
    psa-passwordless_.

``SOCIAL_AUTH_USER_AGENT = None``
    Define the `User-Agent` header value sent to on every request done
    to the service provider, used when combined with a backend that
    sets the `SEND_USER_AGENT` property to `True`. Default value is
    the string `social-auth-<version>`.


Account disconnection
---------------------

Disconnect is an side-effect operation and should be done by POST method only,
some CSRF protection is encouraged (and enforced on Django app). Ensure that
any call to `/disconnect/<backend>/` or `/disconnect/<backend>/<id>/` is done
using POST.

``SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = False``
    When disconnecting an account, it is recommended to trigger a
    token revoke action in the authentication provider, that way we
    inform it that the token won't be used anymore and can be
    disposed. By default the action is not triggered because it's not
    a common option on every provider, and tokens should be disposed
    automatically after a short time.


.. _OpenID PAPE: http://openid.net/specs/openid-provider-authentication-policy-extension-1_0.html
.. _Installation: ../installing.html
.. _Backends: ../backends/index.html
.. _OAuth: http://oauth.net/
.. _passwordless authentication mechanism: https://medium.com/@ninjudd/passwords-are-obsolete-9ed56d483eb
.. _psa-passwordless: https://github.com/omab/psa-passwordless
.. _SESSION_COOKIE_AGE: https://docs.djangoproject.com/en/1.7/ref/settings/#std:setting-SESSION_COOKIE_AGE
.. _a set of regular expressions: https://github.com/python-social-auth/social-core/blob/master/social_core/storage.py#L18-L19
.. _Requests' SSL verification page: https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification
.. _Requests' Proxies page: https://requests.readthedocs.io/en/latest/user/advanced/#proxies