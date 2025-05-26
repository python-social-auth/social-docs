Gitea
======

Gitea supports OAuth2 protocol.

- Register a new application at `Gitea Applications`_.

- Set the callback URL to ``http://example.com/complete/gitea/``
  replacing ``example.com`` with your domain. Drop the trailing slash
  if the project doesn't use it, the URL **must** match the value sent.

- Fill the ``Client ID`` and ``Client Secret`` values from Gitea in the settings::

      SOCIAL_AUTH_GITEA_KEY = ''
      SOCIAL_AUTH_GITEA_SECRET = ''


If your Gitea setup resides in another domain, then add the following setting::

  SOCIAL_AUTH_GITEA_API_URL = 'https://example.com'

it must be the **full url** to your Gitea setup.

.. _Gitea Applications: https://gitea.com/user/settings/applications
