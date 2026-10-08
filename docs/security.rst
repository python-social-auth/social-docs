Security considerations
=======================

Stable social account identifiers
---------------------------------

Social authentication associations are authorization bindings. Their ``uid``
must therefore come from a provider identifier that is immutable and cannot be
reassigned, rather than a display name, email address, UPN, or other
human-readable login name.

Bundled backends use stable provider identifiers where available, including
OIDC ``sub`` claims, provider account IDs, UUIDs, and verified OpenID identity
URLs. Applications overriding a backend's ``ID_KEY`` are responsible for
ensuring the selected claim has the same stability properties. Backends whose
provider responses expose no stable identifier, including Drip, Last.fm, and
Mixcloud, are association-only and require an authenticated local user.

When upgrading an existing deployment, read
:doc:`configuration/identifier-migration` before authenticating users. Candidate
lookup uses historical keys and values; authorization to migrate requires
matching stored current-identifier evidence. Conflicting evidence always blocks
migration.

Only audited historical transitions that lacked evidence retain default
unverified migration. This compatibility allowance accepts a first-login race
through mutable identifiers. Security-sensitive deployments should set
``SOCIAL_AUTH_ALLOW_UNVERIFIED_LEGACY_UID_MIGRATION = False`` and use recovery
or authenticated linking where evidence is unavailable. Explicit ``True`` is an
unsafe escape hatch, not a verification mechanism. Configuration-driven changes
and custom backends require evidence by default.


Host header validation
----------------------

The library may use the incoming HTTP ``Host`` header when generating absolute URLs
or redirects during the authentication and authorization flow. If the ``Host``
header is not validated by the deployment stack, it may allow host header
injection attacks.

This is a deployment and configuration concern rather than a defect in the
library itself. The behavior is intentional, as the library needs to construct
absolute URLs for OAuth callbacks and redirects. Proper upstream validation is
required to ensure that only legitimate ``Host`` header values are accepted by your
application.


Reverse proxy configuration
----------------------------

When deploying behind a reverse proxy (such as nginx, Apache, HAProxy, or a
cloud load balancer), the proxy must validate the Host header before forwarding
requests to the application.

Key requirements:

* **Validate the Host header**: Only expected hostnames should be forwarded
  upstream to the application. Requests with unexpected or malicious Host
  values should be rejected by the proxy.

* **Forwarded headers**: If your deployment uses forwarded headers such as
  ``X-Forwarded-Host`` or the standard ``Forwarded`` header:

  * These headers must be accepted **only from trusted proxies**.
  * They must **not** be blindly trusted from direct client requests.
  * They must be configured explicitly in the proxy configuration.

.. note::

   Configuration syntax varies across reverse
   proxy implementations. Consult your proxy's documentation for Host header
   validation and forwarded header handling.


Django configuration
--------------------

When using Python Social Auth with Django, proper Host header validation must
be configured at the application level using Django's built-in security
features.

Key requirements:

* **Configure ALLOWED_HOSTS**: The ``ALLOWED_HOSTS`` setting must be explicitly
  configured with the canonical hostname(s) for your application. For example::

    ALLOWED_HOSTS = ['example.com', 'www.example.com']

* **Never use wildcard in production**: The wildcard value ``"*"`` must not be
  used in production environments, as it disables Host header validation
  entirely.

* **Host validation behind proxies**: Host validation must remain enabled even
  when the application is deployed behind a reverse proxy. Do not disable
  ``ALLOWED_HOSTS`` validation based on the assumption that the proxy will
  handle it.

* **Forwarded header settings**: If your deployment uses forwarded headers,
  configure Django's ``USE_X_FORWARDED_HOST`` setting carefully. This setting
  should only be enabled when:

  * The application is behind a trusted reverse proxy.
  * The proxy is properly configured to set or strip forwarded headers.
  * The proxy prevents clients from sending malicious forwarded headers
    directly.

For more information on Django security settings, refer to the `Django security
documentation`_.

.. _Django security documentation: https://docs.djangoproject.com/en/stable/topics/security/
