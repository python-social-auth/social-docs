Podio
=====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``podio``
     - ``social_core.backends.podio.PodioOAuth2``

Podio offers OAuth2 as their auth mechanism. In order to enable it, follow:

- Register a new application at `Podio API Keys`_

- Fill **Client Id** and **Client Secret** values::

      SOCIAL_AUTH_PODIO_KEY = ''
      SOCIAL_AUTH_PODIO_SECRET = ''

.. _Podio API Keys: https://developers.podio.com/api-key
