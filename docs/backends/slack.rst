Slack
=====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``slack``
     - ``social_core.backends.slack.SlackOAuth2``

Slack

- Register a new application at Slack_, set the callback URL to
  ``http://example.com/complete/slack/`` replacing ``example.com`` with your
  domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_SLACK_KEY = ''
      SOCIAL_AUTH_SLACK_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_SLACK_SCOPE = [...]

  See auth scopes at `Slack OAuth docs`_.

- Limiting by team is possible by::

    SOCIAL_AUTH_SLACK_TEAM = ''

.. _Slack: https://api.slack.com/applications
.. _Slack OAuth docs: https://api.slack.com/docs/oauth
