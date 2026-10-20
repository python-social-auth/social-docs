EVE Online Single Sign-On (SSO)
===============================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``eveonline``
     - ``social_core.backends.eveonline.EVEOnlineOAuth2``

The EVE Single Sign-On (SSO) works similar to GitHub (OAuth2).

- Register a new application at `EVE Developers`_, set the callback URL to
  ``http://example.com/complete/eveonline/`` replacing ``example.com`` with your
  domain.

- Fill the ``Client ID`` and ``Secret Key`` values from EVE Developers in the settings::

      SOCIAL_AUTH_EVEONLINE_KEY = ''
      SOCIAL_AUTH_EVEONLINE_SECRET = ''

- If you want to use EVE Character names as user names, use this setting::

      SOCIAL_AUTH_CLEAN_USERNAMES = False

- If you want to access EVE Online's CREST API, use::

      SOCIAL_AUTH_EVEONLINE_SCOPE = ['publicData']

Character transfers
-------------------

EVE characters can move between player accounts. This backend checks the
``CharacterOwnerHash`` returned by EVE SSO against the hash saved with an
existing ``CharacterID`` association. If the hashes differ, sign-in fails with
``identity_in_use``; the transferred character cannot access the previous
owner's local account.

To let the new owner sign in, an administrator must verify the transfer and
remove the old social-auth association. The new owner can then sign in with the
character and create or link their own local account. Preserve access to any
other identities and data on the previous owner's local account when removing
the association.

An older association without a saved ``owner_hash`` records the hash from its
next successful sign-in. Because that row has no evidence of the previous
owner, review such rows before relying on this backfill in sensitive
deployments. Sign-in fails if EVE SSO omits ``CharacterOwnerHash``.

.. _EVE Developers: https://developers.eveonline.com/
