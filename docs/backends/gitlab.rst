GitLab
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
   * - ``gitlab``
     - ``social_core.backends.gitlab.GitLabOAuth2``

GitLab supports OAuth2 protocol.

- Register a new application at `GitLab Applications`_.

- Set the callback URL to ``http://example.com/complete/gitlab/``
  replacing ``example.com`` with your domain. Drop the trailing slash
  if the project doesn't use it, the URL **must** match the value sent.

- Ensure to mark the ``read_user`` scope. If marking ``api`` scope too, define::

    SOCIAL_AUTH_GITLAB_SCOPE = ['api']

- Fill the ``Client ID`` and ``Client Secret`` values from GitLab in the settings::

      SOCIAL_AUTH_GITLAB_KEY = ''
      SOCIAL_AUTH_GITLAB_SECRET = ''


If your GitLab setup resides in another domain, then add the following setting::

  SOCIAL_AUTH_GITLAB_API_URL = 'https://example.com'

it must be the **full url** to your GitLab setup.

.. _GitLab Applications: https://gitlab.com/-/profile/applications
