Evernote OAuth
==============

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``evernote``
     - ``social_core.backends.evernote.EvernoteOAuth``

Evernote uses OAuth 1.0 for its production authentication workflow.

- Register a new application at `Evernote API Key form`_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_EVERNOTE_KEY = ''
      SOCIAL_AUTH_EVERNOTE_SECRET = ''


.. _Evernote API Key form: http://dev.evernote.com/support/api_key.php
