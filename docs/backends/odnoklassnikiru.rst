Odnoklassniki.ru
================

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``odnoklassniki-oauth2``
     - ``social_core.backends.odnoklassniki.OdnoklassnikiOAuth2``
   * - ``odnoklassniki-app``
     - ``social_core.backends.odnoklassniki.OdnoklassnikiApp``

There are two options with Odnoklassniki: either you use OAuth2 workflow to
authenticate odnoklassniki users at external site, or you authenticate users
within your IFrame application.

OAuth2
------

If you use OAuth2 workflow, you need to:

- register a new application with `OAuth registration form`_

- fill out some settings::

    SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_KEY = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_SECRET = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_OAUTH2_PUBLIC_NAME = ''

- add ``'social_core.backends.odnoklassniki.OdnoklassnikiOAuth2'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.


IFrame applications
-------------------

If you want to authenticate users in your IFrame application,

- read `Rules for application developers`_

- fill out `Developers registration form`_

- get your personal sandbox

- fill out some settings::

    SOCIAL_AUTH_ODNOKLASSNIKI_APP_KEY = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_APP_SECRET = ''
    SOCIAL_AUTH_ODNOKLASSNIKI_APP_PUBLIC_NAME = ''

- add ``'social_core.backends.odnoklassniki.OdnoklassnikiApp'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``

- sign a public offer and do some bureaucracy

You may also use::

    SOCIAL_AUTH_ODNOKLASSNIKI_APP_EXTRA_USER_DATA_LIST

Defaults to empty tuple, for the list of available fields see `Documentation on user.getInfo`_

The IFrame launch parameters are signed by Odnoklassniki, but they are not
bound to an authentication request initiated by the receiving browser and do
not provide an age limit or single-use protection. Consequently,
``odnoklassniki-app`` does not create account associations from an already
authenticated local session. Such a launch is accepted only when its OK
identity is already associated with the same local user.

Use the state-bound ``odnoklassniki-oauth2`` backend when a user needs to link
a new Odnoklassniki identity to an existing local account. Applications that
require protection against login CSRF or replay for anonymous IFrame launches
must add an application-level initiation and single-use confirmation step.

.. _OAuth registration form: https://apiok.ru/wiki/pages/viewpage.action?pageId=42476652
.. _Rules for application developers: https://apiok.ru/wiki/display/ok/Odnoklassniki.ru+Third+Party+Platform
.. _Developers registration form: https://apiok.ru/wiki/pages/viewpage.action?pageId=5668937
.. _Documentation on user.getInfo: https://apiok.ru/wiki/display/ok/REST+API+-+users.getInfo
