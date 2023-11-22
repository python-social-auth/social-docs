Adding a new backend
====================

Adding new backends is quite easy.  Usually just all that's required is to add
a ``class`` with a couple of settings and method overrides to retrieve user data
from a services API. Follow the details below:


Common attributes
-----------------

First, let's check the common attributes for all backend types.

``name = ''``
    Any backend needs a name, usually the popular name of the service is used,
    like ``facebook``, ``twitter``, etc. It must be unique, otherwise another
    backend can take precedence if it's listed before in the
    ``AUTHENTICATION_BACKENDS`` setting.

``ID_KEY = None``
    Defines the attribute in the service response that identifies the user as
    unique to the service, the value is later stored in the ``uid`` attribute
    in the ``UserSocialAuth`` instance.

``REQUIRES_EMAIL_VALIDATION = False``
    Flags the backend to enforce email validation during the pipeline (if the
    corresponding pipeline ``social_core.pipeline.mail.mail_validation`` was
    enabled).

``EXTRA_DATA = None``
    During the auth process some basic user data is returned by the provider or
    retrieved by the ``user_data()`` method which usually is used to call some API
    on the provider to retrieve it. This data will be stored in the
    ``UserSocialAuth.extra_data`` attribute, but to make it accessible under
    some common names on different providers, this attribute defines a list of
    tuples in the form ``(name, alias)`` where ``name`` is the key in the user
    data (which should be a ``dict`` instance) and ``alias`` is the name to
    store it on ``extra_data``.

``ACCESS_TOKEN_METHOD = 'GET'``
    Specifying the method type required to retrieve your access token if it's not
    the default GET request.


OAuth
-----

OAuth1 and OAuth2 provide some common definitions based on the shared
behavior during the auth process.  For example, a successful API response from
``AUTHORIZATION_URL`` usually returns some basic user data like a user Id.


Shared attributes
*****************

``name``
    This defines the backend name and identifies it during the auth process.
    The name is used in the URLs ``/login/<backend name>`` and
    ``/complete/<backend name>``.

``ID_KEY = 'id'``
    The default key name where the user identification field is defined, it's used
    in the auth process when some basic user data is returned. This Id is stored
    in the ``UserSocialAuth.uid`` field and this, together with the
    ``UserSocialAuth.provider`` field, is used to uniquely identify a user
    association.

``SCOPE_PARAMETER_NAME = 'scope'``
    The scope argument is used to tell the provider the API endpoints you want to
    call later, it's a permissions request granted over the ``access_token``
    later retrieved. The default value is ``scope`` since that's usually the name
    used in the URL parameter, but can be overridden if needed.

``DEFAULT_SCOPE = None``
    Some providers give nothing about the user but some basic data like the user
    Id or an email address. The default scope attribute is used to specify a
    default value for the ``scope`` argument to request those extra bits.

``SCOPE_SEPARATOR = ' '``
    The ``scope`` argument is usually a list of permissions to request, the
    list is joined with a separator, usually just a blank space, but this can differ
    from provider to provider.  Override the default value with this attribute
    if it differs.


OAuth2
******

OAuth2 backends are fairly simple to implement; just a few settings, a method
override and it's mostly ready to go.

The key points on these backends are:

``AUTHORIZATION_URL``
    This is the entry point for the authorization mechanism, users must be
    redirected to this URL, used on ``auth_url`` method which builds the
    redirect address with ``AUTHORIZATION_URL`` plus some arguments
    (``client_id``, ``redirect_uri``, ``response_type``, and ``state``).

``ACCESS_TOKEN_URL``
    Must point to the API endpoint that provides an ``access_token`` needed to
    authenticate in users behalf on future API calls.

``REFRESH_TOKEN_URL``
    Some providers give the option to renew the ``access_token`` since they are
    usually limited in time, once that time runs out, the token is invalidated
    and cannot be used anymore. This attribute should point to that API
    endpoint.

``RESPONSE_TYPE``
    The response type expected on the auth process, default value is ``code``
    as dictated by OAuth2 definition. Override it if default value doesn't fit
    the provider implementation.

``STATE_PARAMETER``
    OAuth2 defines that a ``state`` parameter can be passed in order to
    validate the process, it's kind of a CSRF check to avoid man in the middle
    attacks. Some don't recognise it or don't return it which will make the
    auth process invalid. Set this attribute to ``False`` in that case.

``REDIRECT_STATE``
    For those providers that don't recognise the ``state`` parameter, the app
    can add a ``redirect_state`` argument to the ``redirect_uri`` to mimic it.
    Set this value to ``False`` if the provider likes to verify the
    ``redirect_uri`` value and this parameter invalidates that check.


Example code::

    from social_core.backends.oauth import BaseOAuth2

    class GitHubOAuth2(BaseOAuth2):
        """GitHub OAuth authentication backend"""
        name = 'github'
        AUTHORIZATION_URL = 'https://github.com/login/oauth/authorize'
        ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
        ACCESS_TOKEN_METHOD = 'POST'
        SCOPE_SEPARATOR = ','
        EXTRA_DATA = [
            ('id', 'id'),
            ('expires', 'expires')
        ]

        def get_user_details(self, response):
            """Return user details from GitHub account"""
            return {'username': response.get('login'),
                    'email': response.get('email') or '',
                    'first_name': response.get('name')}

        def user_data(self, access_token, *args, **kwargs):
            """Loads user data from service"""
            url = 'https://api.github.com/user?' + urlencode({
                'access_token': access_token
            })
            return self.get_json(url)


OAuth2 with PKCE
*****************

This is simply an extension of OAuth2 adding `Proof Key for Code Exchange (PKCE)`_ which provides security against authorization code interception attack.

Use the ``BaseOAuth2PKCE`` class as a drop-in replacement for ``BaseOAuth2`` for implementing backends that support PKCE. For reference, you may refer to `Bitbucket Data Center OAuth2`_ and `Twitter OAuth2`_ as example implementations.

Only a single key atttribute is needed on these backends:

``PKCE_DEFAULT_CODE_CHALLENGE_METHOD``
    Depends on which code challenge method is supported by the provider.
    The possible values for this are ``s256`` and ``plain``.
    By default, ``s256`` is set.


OAuth1
******

OAuth1 process is a bit more trickier, `Twitter Docs`_ explains it quite well.
Besides the ``AUTHORIZATION_URL`` and ``ACCESS_TOKEN_URL`` attributes, a third
one is needed used when starting the process.

``REQUEST_TOKEN_URL = ''``
    During the auth process an unauthorized token is needed to start the
    process, later this token is exchanged for an ``access_token``. This
    setting points to the API endpoint where that unauthorized token can be
    retrieved.

Example code::

    from xml.dom import minidom

    from social_core.backends.oauth import ConsumerBasedOAuth


    class TripItOAuth(ConsumerBasedOAuth):
        """TripIt OAuth authentication backend"""
        name = 'tripit'
        AUTHORIZATION_URL = 'https://www.tripit.com/oauth/authorize'
        REQUEST_TOKEN_URL = 'https://api.tripit.com/oauth/request_token'
        ACCESS_TOKEN_URL = 'https://api.tripit.com/oauth/access_token'
        EXTRA_DATA = [('screen_name', 'screen_name')]

        def get_user_details(self, response):
            """Return user details from TripIt account"""
            try:
                first_name, last_name = response['name'].split(' ', 1)
            except ValueError:
                first_name = response['name']
                last_name = ''
            return {'username': response['screen_name'],
                    'email': response['email'],
                    'fullname': response['name'],
                    'first_name': first_name,
                    'last_name': last_name}

        def user_data(self, access_token, *args, **kwargs):
            """Return user data provided"""
            url = 'https://api.tripit.com/v1/get/profile'
            request = self.oauth_request(access_token, url)
            content = self.fetch_response(request)
            try:
                dom = minidom.parseString(content)
            except ValueError:
                return None

            return {
                'id': dom.getElementsByTagName('Profile')[0].getAttribute('ref'),
                'name': dom.getElementsByTagName(
                    'public_display_name')[0].childNodes[0].data,
                'screen_name': dom.getElementsByTagName(
                    'screen_name')[0].childNodes[0].data,
                'email': dom.getElementsByTagName(
                    'is_primary')[0].parentNode.getElementsByTagName(
                    'address')[0].childNodes[0].data,
            }


OpenID
------

OpenID is far simpler than OAuth since it's used for authentication rather
than authorization (regardless it's used for authorization too).

A single attribute is usually needed, the authentication URL endpoint.

``URL = ''``
    OpenID endpoint where to redirect the user.

Sometimes the URL is user dependant, like in myOpenID_ where the URL is
``https://<user handler>.myopenid.com``. For those cases where the user must
input it's handle (or full URL). The backend must override the ``openid_url()``
method to retrieve it and return a full URL to where the user will be
redirected.

Example code::

    from social_core.backends.open_id import OpenIdAuth
    from social_core.exceptions import AuthMissingParameter


    class LiveJournalOpenId(OpenIdAuth):
        """LiveJournal OpenID authentication backend"""
        name = 'livejournal'

        def get_user_details(self, response):
            """Generate username from identity url"""
            values = super(LiveJournalOpenId, self).get_user_details(response)
            values['username'] = values.get('username') or \
                                 urlparse.urlsplit(response.identity_url)\
                                            .netloc.split('.', 1)[0]
            return values

        def openid_url(self):
            """Returns LiveJournal authentication URL"""
            if not self.data.get('openid_lj_user'):
                raise AuthMissingParameter(self, 'openid_lj_user')
            return 'http://%s.livejournal.com' % self.data['openid_lj_user']


Auth APIs
---------

For others authentication types, a ``BaseAuth`` class is defined to help. Those
custom auth methods must override the ``auth_url()`` and ``auth_complete()``
methods.

Example code::

    from google.appengine.api import users

    from social_core.backends.base import BaseAuth
    from social_core.exceptions import AuthException


    class GoogleAppEngineAuth(BaseAuth):
        """GoogleAppengine authentication backend"""
        name = 'google-appengine'

        def get_user_id(self, details, response):
            """Return current user id."""
            user = users.get_current_user()
            if user:
                return user.user_id()

        def get_user_details(self, response):
            """Return user basic information (id and email only)."""
            user = users.get_current_user()
            return {'username': user.user_id(),
                    'email': user.email(),
                    'fullname': '',
                    'first_name': '',
                    'last_name': ''}

        def auth_url(self):
            """Build and return complete URL."""
            return users.create_login_url(self.redirect_uri)

        def auth_complete(self, *args, **kwargs):
            """Completes login process, must return user instance."""
            if not users.get_current_user():
                raise AuthException('Authentication error')
            kwargs.update({'response': '', 'backend': self})
            return self.strategy.authenticate(*args, **kwargs)


.. _Twitter Docs: https://dev.twitter.com/docs/auth/implementing-sign-twitter
.. _myOpenID: https://www.myopenid.com/
.. _Proof Key for Code Exchange (PKCE): https://datatracker.ietf.org/doc/html/rfc7636
.. _Bitbucket Data Center OAuth2: https://github.com/python-social-auth/social-core/blob/master/social_core/backends/bitbucket_datacenter.py
.. _Twitter OAuth2: https://github.com/python-social-auth/social-core/blob/master/social_core/backends/twitter_oauth2.py