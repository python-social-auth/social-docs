OpenID
======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``openid``
     - ``social_core.backends.open_id.OpenIdAuth``

OpenID_ support is simpler to implement than OAuth_. Google and Yahoo
providers are supported by default, others are supported by POST method
providing endpoint URL.

The generic OpenID backend stores the identity URL asserted by the provider as
the user's unique identifier. Because this identifier is protocol-derived
rather than selected from a response mapping, the generic ``ID_KEY`` setting
does not apply.

Provider binding
----------------

OpenID backends configured for one provider require the authentication flow to
start in the same browser session that receives the callback. The callback's
``openid.op_endpoint`` and the endpoint verified by the OpenID consumer must
exactly match the HTTPS endpoint discovered at the start of that flow. A
missing session, a cleartext endpoint, or a different provider requires the
user to restart authentication.

This requirement applies to the bundled Ubuntu, openSUSE, Yandex, Launchpad,
Fedora, Belgium eID, OpenStack, OpenInfra, LiveJournal, and Steam backends. The
generic ``openid`` backend remains provider-selectable because the application
user supplies its provider URL.

Custom backends with a fixed ``URL`` receive provider binding automatically.
A custom backend that computes a fixed-provider URL in ``openid_url()`` must
override ``requires_openid_provider_binding()`` to return ``True``. Provider
discovery URLs and discovered provider endpoints must use HTTPS; there is no
setting to disable this validation.

OpenID_ backends can store extra data in ``UserSocialAuth.extra_data`` field
by defining a set of values names to retrieve from any of the used schemas,
AttributeExchange and SimpleRegistration. As their keywords differ we need
two settings.

Settings is per backend, so we have two possible values for each one. Name
is dynamically checked using uppercase backend name as prefix::

    SOCIAL_AUTH_<uppercase backend name>_SREG_EXTRA_DATA
    SOCIAL_AUTH_<uppercase backend name>_AX_EXTRA_DATA

Example::

    SOCIAL_AUTH_GOOGLE_SREG_EXTRA_DATA = [(..., ...)]
    SOCIAL_AUTH_GOOGLE_AX_EXTRA_DATA = [(..., ...)]

Settings must be a list of tuples mapping value name in response and value
alias used to store. A third value (boolean) is supported to, it's purpose is
to signal if the value should be discarded if it evaluates to ``False``, this
is to avoid replacing old (needed) values when they don't form part of current
response. If not present, then this check is avoided and the value will replace
any data.

Username
--------

The OpenID_ backend will check for a ``username`` key in the values returned by
the server, but default to ``first-name`` + ``last-name`` if that key is
missing. It's possible to indicate the username key in the values If the
username is under a different key with a setting, but backends should have
defined a default value. For example::

    SOCIAL_AUTH_FEDORA_USERNAME_KEY = 'nickname'

This setting indicates that the username should be populated by the
``nickname`` value in the Fedora OpenID_ provider.

.. _OpenID: http://openid.net/
.. _OAuth: http://oauth.net/
