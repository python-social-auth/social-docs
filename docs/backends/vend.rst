Lightspeed Retail (X-Series)
============================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``vend``
     - ``social_core.backends.vend.VendOAuth2``

Vend supports OAuth 2.

The backend requests the ``users:read`` scope by default. Lightspeed requires
a non-empty ``scope`` parameter for new OAuth authorizations, and the current
user endpoint requires ``users:read``. If you override
``SOCIAL_AUTH_VEND_SCOPE`` or disable default scopes, include
``users:read``. Existing grants without this permission may need users to
authorize the application again.
See Lightspeed's `current user API`_ and `scope requirement`_ for the
provider contract.

The backend now identifies the user who authorized the access token rather
than the first user in the shop's user list. Deployments with prior Vend
associations should compare each stored shop/user pair with the authorizing
user returned by the current-user endpoint. A conflict rejects login. Confirm
the local account owner through another sign-in or independently verified
recovery method, then remove the stale association and let that owner authorize
Vend again. Do not reassign a row using only a shop ID or display name.

- Register a new application at `Vend Developers Portal`_

- Add the Vend OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.vend.VendOAuth2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_VEND_OAUTH2_KEY = ''
      SOCIAL_AUTH_VEND_OAUTH2_SECRET = ''

More details on their docs_.

.. _Vend Developers Portal: https://developers.vendhq.com/developer/applications
.. _docs: https://developers.vendhq.com/documentation
.. _current user API: https://x-series-api.lightspeedhq.com/v1.0/reference/getuser
.. _scope requirement: https://x-series-api.lightspeedhq.com/changelog/2025-11-scope-parameter-required
