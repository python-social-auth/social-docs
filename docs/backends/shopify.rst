Shopify
=======

Shopify uses OAuth 2 for authentication.

To use this backend, you must:

- Install the `Shopify python library`_::
  
    pip install --upgrade ShopifyAPI

- Register a new application at `Shopify Partners`_
- Configure your Shopify app to use the application URL of `https://[your domain]/login/shopify/`
- Configure your Shopify app to use the callback URL of `https://[your domain]/complete/shopify/`
- If you're using Django, add the backend to your AUTHENTICATION_BACKENDS configuration::
  
    AUTHENTICATION_BACKENDS = (
        ...,
        'social_core.backends.shopify.ShopifyOAuth2',
        ...,
    )
    
- fill ``API Key`` and ``Shared Secret`` values in your django settings::

      SOCIAL_AUTH_SHOPIFY_KEY   = ''
      SOCIAL_AUTH_SHOPIFY_SECRET = ''

- fill the scope permissions that you require into the settings `Shopify API`_::

      SOCIAL_AUTH_SHOPIFY_SCOPE = ['write_script_tags',
                                   'read_orders',
                                   'write_customers',
                                   'read_products']

- If you'd like to, you can set your desired Shopify API version in your settings::
      
      SOCIAL_AUTH_SHOPIFY_API_VERSION = '2020-10'
      
`ShopifyAPI 5.0.0`_ introduced a non backward compatible change in order to
support Shopify API versioning. The backend will default to value `2019-04` but
it's possible to override the default with the following setting::

    SOCIAL_AUTH_SHOPIFY_API_VERSION = 'unstable'

.. _Shopify Partners: http://www.shopify.com/partners
.. _Shopify API: http://api.shopify.com/authentication.html#scopes
.. _Shopify python library: https://github.com/Shopify/shopify_python_api
.. _ShopifyAPI 5.0.0: https://github.com/Shopify/shopify_python_api#-breaking-change-notice-for-version-500-
