Udata
=====

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
