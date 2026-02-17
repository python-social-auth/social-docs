Security considerations
=======================

The library may use the incoming HTTP Host header when generating absolute URLs
or redirects during the authentication and authorization flow. If the Host
header is not validated by the deployment stack, it may allow host header
injection attacks.

This is a deployment and configuration concern rather than a defect in the
library itself. The behavior is intentional, as the library needs to construct
absolute URLs for OAuth callbacks and redirects. Proper upstream validation is
required to ensure that only legitimate Host header values are accepted by your
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
