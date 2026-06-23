Meetup
======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``meetup``
     - ``social_core.backends.meetup.MeetupOAuth2``

Meetup.com uses OAuth2 for its auth mechanism.

- Register a new OAuth Consumer at `Meetup Consumer Registration`_, set your
  consumer name, redirect uri.

- Fill ``key`` and ``secret`` values in the settings::

      SOCIAL_AUTH_MEETUP_KEY = ''
      SOCIAL_AUTH_MEETUP_SECRET = ''

.. _Meetup Consumer Registration: https://secure.meetup.com/meetup_api/oauth_consumers/create
