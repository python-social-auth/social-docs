OAuth
=====

OAuth_ communication demands a set of keys exchange to validate the client
authenticity prior to user approbation. Twitter, and Facebook facilitates
these keys by application registration, Google works the same,
but provides the option for unregistered applications.

Check next sections for details.

OAuth_ backends also can store extra data in ``UserSocialAuth.extra_data``
field by defining a set of values names to retrieve from service response.

Settings is per backend and its name is dynamically checked using uppercase
backend name as prefix::

    SOCIAL_AUTH_<uppercase backend name>_EXTRA_DATA

Example::

    SOCIAL_AUTH_FACEBOOK_EXTRA_DATA = [(..., ...)]

Settings must be a list of tuples mapping value name in response and value
alias used to store. A third value (boolean) is supported, its purpose is
to signal if the value should be discarded if it evaluates to ``False``, this
is to avoid replacing old (needed) values when they don't form part of current
response. If not present, then this check is avoided and the value will replace
any data.


.. _oauth-token-renewal:

Token renewal
-------------

Use the stored social account to renew credentials explicitly::

    social.refresh_token(strategy=strategy)

To renew only when the stored access token has expired, use::

    access_token = social.get_access_token(strategy)

Tokens with five seconds or less remaining are considered expired. The
backend selects the renewal credential through ``get_refresh_token()``.
Standard OAuth2 backends require a nonempty stored ``refresh_token``; they
never send an access token in its place. Facebook OAuth2 and Facebook App
instead exchange the stored access token using ``fb_exchange_token``.

When no renewal credential is available, ``refresh_token()`` raises
``AuthCredentialError`` with ``code='reauthentication_required'``,
``source='storage'``, ``stage='refresh'``, and ``recovery='reauthenticate'``
if the stored access token is known to have expired. ``get_access_token()``
propagates this error. Applications should catch this credential error and
arrange another provider login. See :doc:`/exceptions`.

If expiry is unknown or the access token is still valid, an explicit refresh
without a renewal credential returns without a request or changes to stored
credentials. ``get_access_token()`` returns the stored access token in those
cases; unknown expiry does not guarantee the token remains valid. A missing
backend or a backend without a refresh method remains a no-op. Invalid expiry
data raises the existing ``AuthResponseError`` with ``code='invalid_expiry'``.

Refresh tokens are optional. Depending on the provider, requesting one may
require additional scopes such as ``offline_access`` or explicit consent.
Configure these requirements for the provider rather than assuming every login
issues a refresh token.

Backends must store issued refresh tokens in ``EXTRA_DATA``. To retain an
existing token when a refresh response omits a replacement, use::

    EXTRA_DATA = [('refresh_token', 'refresh_token', True)]

Zoom and PayPal, including PayPal Sandbox, store refresh tokens by default and
save replacements returned during renewal. Existing associations that lack a
refresh token require another provider login to obtain and store one.

Migration
~~~~~~~~~

Earlier versions fell back to the access token when no refresh token was
stored. Applications refreshing expired accounts must now handle
``reauthentication_required``. Custom backends that deliberately exchange
access tokens must override ``get_refresh_token()`` as described in
:doc:`implementation`.


.. _OAuth: http://oauth.net/
