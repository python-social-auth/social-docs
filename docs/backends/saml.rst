SAML
====

The SAML backend allows users to authenticate with any provider that supports
the SAML 2.0 protocol (commonly used for corporate or academic single sign on).

The SAML backend for python-social-auth allows your web app to act as a SAML
Service Provider. You can configure one or more SAML Identity Providers that
users can use for authentication. For example, if your users are students, you
could enable Harvard and MIT as identity providers, so that students of either
of those two universities can use their campus login to access your app.

Required Dependency
-------------------

You need to install python3-saml_, this is included in the ``saml`` extra when
installing ``social-core``.

In case you run into ``lxml & xmlsec libxml2 library version mismatch`` error,
it is caused by ``lxml`` being built against a different version of ``libxml2``
than ``xmlsec``. To avoid this, please install both packages from the source
and build them against system libraries:

.. code-block:: sh

   # Install system dependencies
   sudo apt install libxmlsec1-dev

   # Install Python packages from the source
   pip install --no-binary lxml --no-binary xmlsec -e 'social-core[saml]'

Required Configuration
----------------------

At a minimum, you must add the following to your project's settings:

- ``SOCIAL_AUTH_SAML_SP_ENTITY_ID``: The SAML Entity ID for your app. This
  should be a URL that includes a domain name you own. It doesn't matter what
  the URL points to. Example: ``http://saml.yoursite.com``

- ``SOCIAL_AUTH_SAML_SP_PUBLIC_CERT``: The X.509 certificate string for the
  key pair that your app will use. You can generate a new self-signed key pair
  with::

      openssl req -new -x509 -days 3652 -nodes -out saml.crt -keyout saml.key

  The contents of ``saml.crt`` should then be used as the value of this setting
  (you can omit the first and last lines, which aren't required).

- ``SOCIAL_AUTH_SAML_SP_PRIVATE_KEY``: The private key to be used by your app.
  If you used the example openssl command given above, set this to the contents
  of ``saml.key`` (again, you can omit the first and last lines).

- ``SOCIAL_AUTH_SAML_ORG_INFO``: A dictionary that contains information about
  your app. You must specify values for English at a minimum. Each language's
  entry should specify a ``name`` (not shown to the user), a ``displayname``
  (shown to the user), and a URL. See the following
  example::

      {
          "en-US": {
              "name": "example",
              "displayname": "Example Inc.",
              "url": "http://example.com",
          }
      }

- ``SOCIAL_AUTH_SAML_TECHNICAL_CONTACT``: A dictionary with two values,
  ``givenName`` and ``emailAddress``, describing the name and email of a
  technical contact responsible for your app. Example::

      {
          "givenName": "Tech Gal",
          "emailAddress": "technical@example.com"
      }

- ``SOCIAL_AUTH_SAML_SUPPORT_CONTACT``: A dictionary with two values,
  ``givenName`` and ``emailAddress``, describing the name and email of a
  support contact for your app. Example::

      {
          "givenName": "Support Guy",
          "emailAddress": "support@example.com",
      }

- ``SOCIAL_AUTH_SAML_ENABLED_IDPS``: The most important setting. List the Entity
  ID, SSO URL, and x.509 public key certificate for each provider that your app
  wants to support. The SSO URL must support the ``HTTP-Redirect`` binding.
  You can get these values from the provider's XML metadata. Here's an example,
  for TestShib_ (the values come from TestShib's metadata_)::

      {
          "testshib": {
              "entity_id": "https://idp.testshib.org/idp/shibboleth",
              "url": "https://idp.testshib.org/idp/profile/SAML2/Redirect/SSO",
              "x509cert": "MIIEDjCCAvagAwIBAgIBADA ... 8Bbnl+ev0peYzxFyF5sQA==",
          }
      }

  Each IDP can define configuration keys to avoid having to use uniform resource
  name's (ie: ``urn:oid:0.9.2342.19200300.100.1.3`` for email address) as
  attributes to map user details required to complete account creation. The
  values associated with the attr_* keys correspond to the keys specified as
  attributes in the IDP.

  .. important::

     **Version 4.8.0+ Behavior Change:**

     When you explicitly configure an attribute (e.g., ``attr_first_name``), that
     attribute **must** be present in the SAML response from the IdP. If it is
     missing, authentication will fail with an error like:
     ``Missing needed parameter first_name (configured by attr_first_name)``.

     **Options:**

     1. **Remove the configuration** if the attribute is not provided by your IdP.
        The backend will automatically try to map using built-in attribute names.

     2. **Ensure your IdP provides the attribute** with the exact name you configured.

     3. **Use the correct attribute name** from your IdP's SAML response (check
        the actual attribute names sent by your IdP).

  Extending on the "testshib" example::

      {
          "testshib": {
              "entity_id": "https://idp.testshib.org/idp/shibboleth",
              "url": "https://idp.testshib.org/idp/profile/SAML2/Redirect/SSO",
              "x509cert": "MIIEDjCCAvagAwIBAgIBADA ... 8Bbnl+ev0peYzxFyF5sQA==",
              "attr_user_permanent_id": "email",
              "attr_first_name": "first_name",
              "attr_last_name": "last_name",
              "attr_username": "email",
              "attr_email": "email",
          }
      }

  In this example, the attr_user_permanent_id and attr_email are both set to the
  email address passed back in the attribute key 'email'.

  Note: testshib does not provide email as an attribute. This was tested using
  Okta and G Suite (formerly Google Apps for Business).

  **Built-in Attribute Mappings:**

  If you omit the ``attr_*`` configuration keys, the backend will automatically
  try to extract user details using a list of commonly used attribute names,
  including both namespaced URN variants (like
  ``http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname``) and
  simple names (like ``first_name``, ``firstName``, ``given_name``). Missing
  attributes will be silently ignored when using the built-in mappings.

Basic Usage
-----------

- Set all of the required configuration variables described above.

- Generate the SAML XML metadata for your app. The best way to do this is to
  create a new view/page/URL in your app that will call the backend's
  ``generate_metadata_xml()`` method. Here's an example of how to do this in
  Django::

      def saml_metadata_view(request):
          complete_url = reverse('social:complete', args=("saml", ))
          saml_backend = load_backend(
              load_strategy(request),
              "saml",
              redirect_uri=complete_url,
          )
          metadata, errors = saml_backend.generate_metadata_xml()
          if not errors:
              return HttpResponse(content=metadata, content_type='text/xml')

- Download the metadata for your app that was generated by the above method,
  and send it to each Identity Provider (IdP) that you wish to use. Each IdP
  must install and configure your metadata on their system before it will work.

- Now everything is set! To allow users to login with any given IdP, you need to
  give them a link to the python-social-auth "begin"/"auth" URL and include an
  ``idp`` query parameter that specifies the name of the IdP to use. This is
  needed since the backend supports multiple IdPs. The names of the IdPs are the
  keys used in the ``SOCIAL_AUTH_SAML_ENABLED_IDPS`` setting.

  Django example::

      # In view:
      context['testshib_url'] = u"{base}?{params}".format(
          base=reverse('social:begin', kwargs={'backend': 'saml'}),
          params=urllib.urlencode({'next': '/home', 'idp': 'testshib'})
      )
      # In template:
      <a href="{{ testshib_url }}">TestShib Login</a>
      # Result:
      <a href="/login/saml/?next=%2Fhome&amp;idp=testshib">TestShib Login</a>

- Testing with the TestShib_ provider is recommended, as it is known to work
  well.


Advanced Settings
-----------------

- ``SOCIAL_AUTH_SAML_SP_EXTRA``: This can be set to a dict, and any key/value
  pairs specified here will be passed to the underlying ``python-saml`` library
  configuration's ``sp`` setting. Refer to the ``python-saml`` documentation for
  details.

  To publish a rollover certificate in advance of changing, use
  ``SOCIAL_AUTH_SAML_SP_EXTRA`` to set ``['sp']['x509certNew']`` of ``python-saml``::

      {
          "x509certNew": "MIIEDjCCAvagAwIBAgIBADA ... 8Bbnl+ev0peYzxFyF5sQA==",
      }


- ``SOCIAL_AUTH_SAML_SECURITY_CONFIG``: This can be set to a dict, and any
  key/value pairs specified here will be passed to the underlying
  ``python-saml`` library configuration's ``security`` setting. Two useful keys
  that you can set are ``metadataCacheDuration`` and ``metadataValidUntil``,
  which control the expiry time of your XML metadata. By default, a cache
  duration of 10 days will be used, which means that IdPs are allowed to cache
  your metadata for up to 10 days, but no longer. ``metadataCacheDuration`` must
  be specified as an ISO 8601 duration string (e.g. `P1D` for one day).

- ``SOCIAL_AUTH_SAML_EXTRA_DATA``: This can be set to a list of tuples similar
  to the OAuth backend setting. It maps IDP attributes to extra_data attributes.
  Each attribute will be a list of values (even if only 1 value) per how
  python3-saml_ processes attributes::

      SOCIAL_AUTH_SAML_EXTRA_DATA = [('attribute_name', 'extra_data_name_for_attribute'),
                                   ('department', 'department'),
                                   ('manager_full_name', 'manager_full_name')]


Advanced Usage
--------------

You can subclass the ``SAMLAuth`` backend to provide custom functionality. In
particular, there are two methods that are designed for subclasses to override:

- ``get_idp(self, idp_name)``: Given the name of an IdP, return an instance of
  ``SAMLIdentityProvider`` with the details of the IdP. Override this method if
  you wish to use some other method for configuring the available identity
  providers, such as fetching them at runtime from another server, or using a
  list of providers from a Shibboleth federation.

- ``_check_entitlements(self, idp, attributes)``: This method gets called during
  the login process and is where you can decide to accept or reject a user based
  on the user's SAML attributes. For example, you can restrict access to your
  application to only accept users who belong to a certain department. After
  inspecting the passed attributes parameter, do nothing to allow the user to
  login, or raise ``social_core.exceptions.AuthForbidden`` to reject the user.


Troubleshooting
---------------

**Error: "Missing needed parameter first_name (configured by attr_first_name)"**

This error occurs when you have explicitly configured an attribute mapping (like
``attr_first_name``) but your IdP is not providing that attribute in the SAML
response.

**Solution:**

1. **Check what attributes your IdP actually provides.** Inspect the SAML
   response from your IdP to see the exact attribute names being sent.

2. **Remove unused attribute configurations.** If your IdP doesn't provide
   ``first_name``, simply remove ``"attr_first_name": "first_name"`` from your
   configuration. The backend will try to use built-in mappings instead.

3. **Use the correct attribute name.** If your IdP provides the attribute with
   a different name (e.g., ``givenName`` or a namespaced URN like
   ``http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname``), use
   that name in your configuration::

       "attr_first_name": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname",

4. **Configure your IdP** to include the attribute in the SAML response if you
   need it.

**Example:** For Google G Suite SSO, if you're not receiving ``first_name`` and
``last_name`` attributes, remove those configurations and let the backend use
its built-in mappings::

    SOCIAL_AUTH_SAML_ENABLED_IDPS = {
        "gsuite": {
            "entity_id": "...",
            "url": "...",
            "x509cert": "...",
            "attr_user_permanent_id": "email",
            "attr_username": "email",
            "attr_email": "email",
            # Remove attr_first_name and attr_last_name if not provided by IdP
        }
    }

.. _python3-saml: https://github.com/onelogin/python3-saml
.. _TestShib: https://www.testshib.org/
.. _metadata: https://www.testshib.org/metadata/testshib-providers.xml
