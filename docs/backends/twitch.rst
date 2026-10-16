Twitch
======

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``twitch``
     - ``social_core.backends.twitch.TwitchOpenIdConnect``
   * - ``twitch``
     - ``social_core.backends.twitch.TwitchOAuth2``

Twitch works similar to Facebook (OAuth).

- Register a new application in the `connections tab`_ of your Twitch settings
  page, set the callback URL to ``http://example.com/complete/twitch/``
  replacing ``example.com`` with your domain.

- Fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_TWITCH_KEY = ''
      SOCIAL_AUTH_TWITCH_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_TWITCH_SCOPE = [...]

.. _connections tab: http://www.twitch.tv/settings/connections

.. _twitch-identifier-backfill:

Django identifier backfill repair
---------------------------------

Both Twitch backends use the provider name ``twitch``, but OpenID Connect uses
identifier key ``sub`` and OAuth2 uses ``id``. Django migration 0020 in
social-auth-app-django 7.1.0 labelled historical Twitch associations ``id`` for
both variants. Returning OpenID Connect users can consequently receive HTTP 500,
and failed logins can leave additional local users without social associations.

Run migrations through ``0021_repair_twitch_id_keys`` before serving upgraded
authentication traffic. This migration repairs existing databases and fresh
upgrades from before identifier-key tracking. It changes Twitch rows labelled
``id`` to ``sub`` when ``TwitchOpenIdConnect`` is the only built-in Twitch
variant listed in ``AUTHENTICATION_BACKENDS``. If neither or both built-in
variants are listed, it retains the historical ``id`` default. It matches the
exact class paths above without importing configured backends.

``SOCIAL_AUTH_OLD_ID_KEYS["twitch"]`` takes precedence. Before running the
repair, set it to the key used when the existing associations were created if
you use a custom subclass or have changed backend variants. For historical
OpenID Connect associations, use::

    SOCIAL_AUTH_OLD_ID_KEYS = {"twitch": "sub"}

Use ``"id"`` for historical OAuth2 associations. Any value other than ``"sub"``,
including ``None``, prevents the repair. ``None`` also skips Twitch in the
original backfill if it has not yet run. The repair validates the Twitch
override as a nonempty string fitting ``id_key``, or ``None``.

The repair preserves UIDs, account ownership, extra data, timestamps, and labels
other than ``id``. Reversing it preserves corrected labels. Changing settings
after the repair has run does not run it again. Current backend configuration
cannot establish historical usage; review the override before deployment.

Review any local users orphaned by earlier failed logins separately. The
migration does not delete users, because it cannot safely identify which
records resulted from those failures.
