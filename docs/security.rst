Security considerations
=======================

The canonical `social-auth-core threat model`_ and
`social-auth-app-django threat model`_ define each package's trust boundaries,
security guarantees, exceptions, and vulnerability triage rules. This page
provides deployment guidance; detailed configuration and upgrade instructions
live on the linked topic pages.

Trusted configuration and extensions
------------------------------------

Settings, provider endpoints, issuers, signing keys, certificates, algorithms,
proxies, and redirect destinations must come from trusted operator
configuration. Do not let request parameters choose these security policies.
Keep required TLS and protocol validation enabled and use intended HTTPS
provider endpoints. Certificate verification does not protect a cleartext HTTP
endpoint. Retain finite outbound request timeouts.

Custom backends, pipelines, strategies, storage, middleware, and templates run
with application authority. Preserve validation, policy, and association
ordering, and review extensions as security-sensitive code. See
:doc:`backends/implementation`, :doc:`pipeline`, :doc:`strategies`, and
:doc:`storage`.

Provider profile fields are not automatically verified ownership or local
authorization facts. Decide which claims may influence account creation,
updates, groups, email association, and recovery. Escape profile data at output
sinks. Do not enable ``associate_by_email`` without an explicit verified-email
and recovery policy. See :ref:`pipeline-security` and :doc:`groups`.

Stable social account identifiers
---------------------------------

Social associations are authorization bindings. Use stable, provider-scoped
identifiers rather than mutable email addresses, usernames, UPNs, or display
names. Applications overriding ``ID_KEY`` must preserve those properties.
Drip, Last.fm, and Mixcloud expose no suitable stable identifier and are
association-only; they require an authenticated local user.

Read :doc:`configuration/identifier-migration` before upgrading or changing
identifier configuration. It documents evidence requirements, audited
compatibility exceptions, their first-login race, configuration provenance,
and recovery. A missing-evidence compatibility allowance does not establish
continuous ownership. For transferable EVE characters, also read
:doc:`backends/eveonline`.

Sessions and protected transitions
----------------------------------

Use a framework integration supplying isolated sessions, authenticated-user
state, and CSRF protection for local state changes. Preserve the initiating
user through account-linking callbacks; reject or restart a flow if that user
changes. Keep tokens, sessions, associations, codes, nonces, partials, and
backups confidential and protected from modification. The packages do not
provide encryption at rest.

Provider callbacks rely on protocol validation. State, nonce, PKCE, and request
correlation solve different problems; none replaces the others. Some signed
flows do not supply initiation, session binding, or single-use protection.
Review the selected backend's limits, especially :doc:`backends/telegram`,
:doc:`backends/facebook_limited_login`, and legacy iframe flows in
:doc:`backends/vk` and :doc:`backends/odnoklassnikiru`.

For Django, see :doc:`configuration/django` for protected routes and launch
bridges, :doc:`backends/saml` for the SAML browser return flow, and
:ref:`partial-pipeline` for confirmation and template requirements.

.. _oauth2-transaction-state:

OAuth2 transaction state
------------------------

Each OAuth2 authorization start uses a distinct state bound to the initiating
browser session. A callback consumes that transaction before exchanging its
authorization code. Other pending starts in the same session remain valid and
can finish in either order. Expired and repeated callbacks must start again.
OAuth2 authorizations begun before upgrading to this behavior also must restart.

``SOCIAL_AUTH_STATE_LIFETIME`` sets the maximum age in seconds, defaulting to
1800. A provider-specific ``SOCIAL_AUTH_<BACKEND_NAME>_STATE_LIFETIME`` takes
precedence. The value must be a positive integer. Storage integrations must
provide an atomic claim shared across workers; see :ref:`nonce-storage` for
``NonceMixin.consume()`` and :ref:`authentication-storage-cleanup` for Django
cleanup and coordinated upgrade requirements.

For legacy OpenID transaction, discovery, and provider binding, including
upgrade precautions, see :doc:`backends/openid`.

Host headers, redirects, and outbound access
--------------------------------------------

Callback and absolute redirect URLs can be derived from the request host.
Validate ``Host`` against intended application hosts, and accept forwarded
headers only from trusted proxies that set or strip client-supplied values.
Use HTTPS and canonical callback URLs. With Django, configure restrictive
``ALLOWED_HOSTS`` and enable ``USE_X_FORWARDED_HOST`` only with an appropriately
configured trusted proxy. See `Django security documentation`_.

Keep redirect sanitization enabled and restrict approved hosts and schemes.
Explicit private-use schemes authorize by scheme, without host validation.
Redirect checks are not SSRF protection or a general egress policy; see
:ref:`request-redirect-settings`. Generic OpenID deliberately supports
user-selected provider discovery; expose it only if appropriate for the
application and its network policy.

Apply request-size, rate, concurrency, capacity, and retention controls suitable
for the deployment. The packages supply no quantitative resource guarantee.
Constrain provider/discovery egress where required and review access to any
configured credential files. Avoid production debug-pipeline output and
unsafe logging of authentication data; see :ref:`pipeline-security`.

.. _Django security documentation: https://docs.djangoproject.com/en/stable/topics/security/
.. _social-auth-app-django threat model: https://github.com/python-social-auth/social-app-django/blob/master/THREAT_MODEL.md
.. _social-auth-core threat model: https://github.com/python-social-auth/social-core/blob/master/THREAT_MODEL.md
