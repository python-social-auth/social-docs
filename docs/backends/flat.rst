Flat
====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``flat``
     - ``social_core.backends.flat.FlatOAuth2``

`Flat`_ uses OAuth2. In order to enable the backend follow:

- On your project settings, you should add Flat on your
  ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.flat.FlatOAuth2',
    )

- Register an application at `Flat Developer Portal`_

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_FLAT_KEY = ''
    SOCIAL_AUTH_FLAT_SECRET = ''

- Set the ``Callback URL`` to ``http://<your hostname>/complete/flat/``

- Specify `scopes`_ with::

    SOCIAL_AUTH_FLAT_SCOPE = [...]

.. _Flat: https://flat.io
.. _Flat Developer Portal: https://flat.io/developers
.. _scopes: https://flat.io/developers/api/reference/#section/Authentication
