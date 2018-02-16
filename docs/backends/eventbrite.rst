Eventbrite OAuth
================

Eventbrite OAuth 2.0 for its authentication workflow.

- Register a new application at `Account Settings`_ `App Management`_.
    https://www.eventbrite.com/myaccount/apps/

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings using ``Application Key`` and ``OAuth Client Secret`` provided by Eventbrite's created app::

      SOCIAL_AUTH_EVENTBRITE_KEY = '<your Application Key>'
      SOCIAL_AUTH_EVENTBRITE_SECRET = '<your OAuth Client Secret>'


.. _Eventbrite API docs: https://www.eventbrite.com/developer/v3/
