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

Session and provider binding
----------------------------

All OpenID backends require a positive assertion whose provider-signed return
URL carries a session-held, one-use transaction value. The verified response
must also match backend-scoped discovery state from the browser session that
initiated authentication. A second OpenID start in the same session replaces
the first transaction; the earlier callback is rejected. Unsolicited assertions
are rejected, including for anonymous users. Always use the normal backend
initiation path.

When the framework supports restoring sessions, only a session identifier carried
by the provider-signed ``openid.return_to`` can select that session. Missing or
mismatched state requires the user to restart authentication.

The generic ``openid`` backend remains provider-selectable because the
application user supplies its provider URL. Backends configured for one
provider additionally require the callback and verified provider endpoints to
match the exact HTTPS endpoint discovered at initiation. This applies to the
bundled Ubuntu, openSUSE, Yandex, Launchpad, Fedora, Belgium eID, OpenStack,
OpenInfra, LiveJournal, and Steam backends.

Custom backends with a fixed ``URL`` receive provider binding automatically.
A custom backend that computes a fixed-provider URL in ``openid_url()`` must
override ``requires_openid_provider_binding()`` to return ``True``. Provider
discovery URLs and discovered provider endpoints must use HTTPS; there is no
setting to disable this validation. Custom strategies that implement session
restoration must restore the complete OpenID session state and update
session-derived pipeline arguments, including the authenticated user.

Custom backends overriding authorization URL or HTML generation must include
the transaction value in the provider-signed return URL, for example by calling
``_return_to_for_login()``.

Upgrading binding requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Authentication attempts initiated before upgrading to session, transaction, or
fixed-provider binding must restart. Deployments upgrading from a release
without fixed-provider binding should review associations created or migrated
from unexpected identity URLs, especially Ubuntu, openSUSE, and Yandex rows
migrated from nickname or email identifiers. Confirm ownership through recovery
or authenticated relinking; those records cannot be repaired automatically.

Setting ``SOCIAL_AUTH_ALLOW_UNVERIFIED_LEGACY_UID_MIGRATION = False`` limits
migration risk but does not replace provider binding. Disable affected backends
until the fixed release is installed. See
:doc:`../configuration/identifier-migration` for evidence and recovery policy.

Extra data
----------

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
