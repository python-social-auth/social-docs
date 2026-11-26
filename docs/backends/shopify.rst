Shopify
=======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``shopify``
     - ``social_core.backends.shopify.ShopifyOAuth2``

Shopify uses OAuth 2 for store association. A shop domain identifies a store,
not the individual who approved access. Start this backend only for an already
authenticated local user; anonymous Shopify sign-in is rejected. Existing
store associations remain available to their local owners.
Protect the Shopify initiation route with local authentication. If a store
association was previously the only way to sign in, provide another local
sign-in or independently verified account recovery route before upgrading;
then the user can associate the store again from their authenticated session.
If the shop changes owner, independently verify the current owner, remove the
old owner's stale shop association, and only then let the current owner
associate the shop from an authenticated session. Do not transfer the existing
association solely from a shop domain or a claim made in a callback.

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
