Discogs
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
   * - ``discogs``
     - ``social_core.backends.discogs.DiscogsOAuth1``

Discogs uses OAuth v1 for Authentication.

- Register a new application int the `Discogs API settings <_discogs_settings>`_, and

- Add the Discogs backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        "social_core.backends.discogs.DiscogsOAuth1",
        ...
    )

- Add the ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_DISCOGS_KEY = ''
      SOCIAL_AUTH_DISCOGS_SECRET = ''

  Check `Discogs API documentation <_discogs_docs>`_ for details.

.. _discogs_settings: https://www.discogs.com/settings/developers
.. _discogs_docs: https://www.discogs.com/developers/
