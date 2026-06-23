Mendeley
========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``mendeley-oauth2``
     - ``social_core.backends.mendeley.MendeleyOAuth2``

Mendeley supports OAuth2.

In order to support OAuth2:

- Register a new application at `Mendeley Application Registration`_.

- Fill **Application ID** and **Application Secret** values::

      SOCIAL_AUTH_MENDELEY_OAUTH2_KEY = ''
      SOCIAL_AUTH_MENDELEY_OAUTH2_SECRET = ''


.. _Mendeley Application Registration: http://dev.mendeley.com/applications/register/
