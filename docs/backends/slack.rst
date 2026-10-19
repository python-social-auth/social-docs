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

- To allow sign-in only from one Slack workspace, set its workspace ID::

    SOCIAL_AUTH_SLACK_TEAM = 'T0123456789'

  The backend checks the ``team.id`` returned by Slack's ``users.identity``
  response before signing in. The ``team`` authorization parameter selects a
  workspace on Slack's sign-in page, but does not enforce this restriction.
  A missing or different workspace ID rejects the sign-in. Configure a
  workspace ID (starting with ``T``), not a workspace name or Enterprise
  organization ID (starting with ``E``). Deployments previously using a name
  or organization ID must update this setting before upgrading.

.. _Slack: https://api.slack.com/applications
.. _Slack OAuth docs: https://api.slack.com/docs/oauth
