Dropbox
=======

Dropbox supports OAuth2.

- Register a new application at `Dropbox Developers`_.


OAuth2 Api V2
-------------

Add the Dropbox OAuth2 backend to your settings page::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.dropbox.DropboxOAuth2V2',
        ...
    )

- Fill ``App Key`` and ``App Secret`` values in the settings::

      SOCIAL_AUTH_DROPBOX_OAUTH2_KEY = ''
      SOCIAL_AUTH_DROPBOX_OAUTH2_SECRET = ''

.. _Dropbox Developers: https://www.dropbox.com/developers/apps
