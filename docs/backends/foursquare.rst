Foursquare
==========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``foursquare``
     - ``social_core.backends.foursquare.FoursquareOAuth2``

Foursquare uses OAuth2. In order to enable the backend follow:

- Register an application at `Foursquare Developers Portal`_,
  set the ``Redirect URI`` to ``http://<your hostname>/complete/foursquare/``

- Fill in the **Client Id** and **Client Secret** values in your settings::

    SOCIAL_AUTH_FOURSQUARE_KEY = ''
    SOCIAL_AUTH_FOURSQUARE_SECRET = ''

.. _Foursquare Developers Portal: https://foursquare.com/developers/register
