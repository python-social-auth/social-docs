Shopify
=======

Shopify uses OAuth 2 for authentication.

To use this backend, you must install the package ``shopify`` from the `GitHub
project`_. Currently supports v2+

- Register a new application at `Shopify Partners`_, and

- Set the Auth Type to OAuth2 in the application settings

- Set the Application URL to http://[your domain]/login/shopify/

- fill ``API Key`` and ``Shared Secret`` values in your django settings::

      SOCIAL_AUTH_SHOPIFY_KEY   = ''
      SOCIAL_AUTH_SHOPIFY_SECRET = ''

- fill the scope permissions that you require into the settings `Shopify API`_::

      SOCIAL_AUTH_SHOPIFY_SCOPE = ['write_script_tags',
                                   'read_orders',
                                   'write_customers',
                                   'read_products']

`ShopifyAPI 5.0.0`_ introduced a non backward compatible change in order to
support Shopify API versioning. The backend will default to value `2019-04` but
it's possible to override the default with the following setting::

    SOCIAL_AUTH_SHOPIFY_API_VERSION = 'unstable'

.. _Shopify Partners: http://www.shopify.com/partners
.. _Shopify API: http://api.shopify.com/authentication.html#scopes
.. _GitHub project: https://github.com/Shopify/shopify_python_api
.. _ShopifyAPI 5.0.0: https://github.com/Shopify/shopify_python_api#-breaking-change-notice-for-version-500-
