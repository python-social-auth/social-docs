Eventbrite OAuth
================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``eventbrite``
     - ``social_core.backends.eventbrite.EventbriteOAuth2``

Eventbrite OAuth 2.0 for its authentication workflow.

- Register a new application at `Account Settings` in `App Management`_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings
  using ``Application Key`` and ``OAuth Client Secret`` provided by
  Eventbrite's created app::

      SOCIAL_AUTH_EVENTBRITE_KEY = '<your Application Key>'
      SOCIAL_AUTH_EVENTBRITE_SECRET = '<your OAuth Client Secret>'


.. _Eventbrite API docs: https://www.eventbrite.com/developer/v3/
.. _App Management: https://www.eventbrite.com/myaccount/apps/
