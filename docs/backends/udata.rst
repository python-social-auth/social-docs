Udata
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
   * - ``datagouv``
     - ``social_core.backends.udata.DatagouvfrOAuth2``

Datagouvfr OAuth2
-----------------

`Datagouvfr`_ supports OAuth2 for their API. In order to set it up:

- Go get your `your API key`_ (previous account creation is required).

- Fill **Consumer Key** and **Consumer Secret** values in settings::

      SOCIAL_AUTH_DATAGOUVFR_KEY = ''
      SOCIAL_AUTH_DATAGOUVFR_SECRET = ''

- Add ``'social_core.backends.udata.DatagouvfrOAuth2'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.

.. _your API key: https://www.data.gouv.fr/fr/admin/me/
.. _Datagouvfr: https://www.data.gouv.fr/
