GitHub
======

GitHub works similar to Facebook (OAuth).

- On your project settings, you should add Github on your ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.github.GithubOAuth2',
    )

- Register a new application at `GitHub Developers`_, set the callback URL to
  ``http://example.com/complete/github/`` replacing ``example.com`` with your
  domain. This will generate a Client Key and a Client Secret.

- Add these values of ``Client ID`` and ``Client Secret`` from GitHub in your project settings file.

The ``Client ID`` should be added on ``SOCIAL_AUTH_GITHUB_KEY`` and the ``Client Secret`` should be
added on ``SOCIAL_AUTH_GITHUB_SECRET``::

      SOCIAL_AUTH_GITHUB_KEY = 'a1b2c3d4'
      SOCIAL_AUTH_GITHUB_SECRET = 'e5f6g7h8i9'

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_GITHUB_SCOPE = [...]

GitHub for Organizations
------------------------

When defining authentication for organizations, use the
``GithubOrganizationOAuth2`` backend instead. The settings are the same as
the non-organization backend, but the names must be::

      SOCIAL_AUTH_GITHUB_ORG_*

Be sure to define the organization name using the setting::

      SOCIAL_AUTH_GITHUB_ORG_NAME = ''

This name will be used to check that the user really belongs to the given
organization and discard it if they're not part of it.


GitHub for Teams
----------------

Similar to ``GitHub for Organizations``, there's a GitHub for Teams backend,
use the backend ``GithubTeamOAuth2``. The settings are the same as
the basic backend, but the names must be::

    SOCIAL_AUTH_GITHUB_TEAM_*

Be sure to define the ``Team ID`` using the setting::

      SOCIAL_AUTH_GITHUB_TEAM_ID = ''

This ``id`` will be used to check that the user really belongs to the given
team and discard it if they're not part of it.


GitHub for Enterprises
----------------------

Check the docs :ref:`github-enterprise` if planning to use GitHub
Enterprises.


GitHub Apps
-----------

Similar to the ``GithubOAuth2`` backend but primarily intended for use
with GitHub applications (non-oauth application type). For GitHub App
applications there are two primary workflows:

1) A person clicks on an icon/button on your website and initiates the
   OAuth login procedure. They will be redirected to GitHub to complete
   the process and then back to your website. The person should be logged-in
   automatically. This is the same workflow as with standard OAuth GitHub apps.

2) A person visits your GitHub App public URL, e.g. ``https://github.com/apps/my-app``.
   They click the **Install** button, select onto which account/organization and
   repositori(es) to install your application and finish the process. GitHub
   will start sending webhooks to the URL you have configured! It will also
   redirect the person to ``Setup URL (optional)``.

- Create a new GitHub App application owned by your organization. e.g.
  ``https://github.com/organizations/python-social-auth/settings/apps/new``

- Set ``User authorization callback URL`` to
  ``http://example.com/complete/github/`` replacing ``example.com`` with your
  domain.

- Turn on ``Request user authorization (OAuth) during installation`` if
  you wish to make ``Setup URL`` equal to ``User authorization callback URL``.
  The side-effect of this is that after installing your GitHub app the person
  will be redirected back to your website and logged in automatically. When
  this is turned on steps 2) and 1) above are executed in sequence.

- Add the values of ``Client ID`` and ``Client Secret`` from GitHub in your
  project settings file as shown above.



.. _GitHub Developers: https://github.com/settings/applications/new
