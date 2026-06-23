Discourse
=========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``discourse``
     - ``social_core.backends.discourse.DiscourseAuth``

Discourse can serve as a Single Sign On provider for Authentication.

- Deploy a Discourse application and `configure
  <https://meta.discourse.org/t/using-discourse-as-a-sso-provider/32974>` the
  application to enable Discourse as an SSO provider.

- Fill in the shared secret and url of the Discourse server in the settings::

      SOCIAL_AUTH_DISCOURSE_SECRET = "myDiscourseSecret"
      SOCIAL_AUTH_DISCOURSE_SERVER_URL = "https://my-discourse-site.com"


Using multiple Discourse instances
----------------------------------

Since Discourse is a distributed application, multiple Discourse instances can
be used as SSO providers. If this is the case, the DiscourseAuth class can be
extended and configured as follows::

      from social_core.backends.discourse import DiscourseAuth

      class DiscourseAuthFoo(DiscourseAuth):
          name = 'discourse-foo'

      class DiscourseAuthBar(DiscourseAuth):
          name = 'discourse-bar'

Fill in the settings like so::

      SOCIAL_AUTH_DISCOURSE_FOO_SECRET = "myDiscourseFooSecret"
      SOCIAL_AUTH_DISCOURSE_FOO_SERVER_URL = "https://my-discourse-foo-site.com"
      SOCIAL_AUTH_DISCOURSE_BAR_SECRET = "myDiscourseBarSecret"
      SOCIAL_AUTH_DISCOURSE_BAR_SERVER_URL = "https://my-discourse-bar-site.com"
