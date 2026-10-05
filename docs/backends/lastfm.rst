Last.fm
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
   * - ``lastfm``
     - ``social_core.backends.lastfm.LastFmAuth``

Last.fm uses a similar authentication process than OAuth2 but it's not. In
order to enable the support for it just:

- Register an application at `Get an API Account`_, set the Last.fm callback to
  something sensible like http://your.site/complete/lastfm

- Fill in the **API Key** and **API Secret** values in your settings::

    SOCIAL_AUTH_LASTFM_KEY = ''
    SOCIAL_AUTH_LASTFM_SECRET = ''

- Enable the backend in ``AUTHENTICATION_BACKENDS`` setting.

Last.fm does not expose a stable account identifier in its authentication
session response. The backend is therefore association-only: an authenticated
local user must initiate and complete the connection. Last.fm cannot create a
local user or authenticate a logged-out user.

.. _Get an API Account: http://www.last.fm/api/account/create
