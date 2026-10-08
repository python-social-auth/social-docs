.. _identifier-migration:

Identifier migration
====================

Authentication looks up the current ``(provider, id_key, uid)`` first. If it
does not exist, it looks up previous keys and their values from the authenticated
provider response. These queries use the existing provider/UID index; they do
not search every association's JSON data. Empty-key historical rows are also
considered using the same indexed UID lookups.

An old email or username locates a candidate, but does not prove that the
candidate belongs to the current provider account. The candidate's saved current
identifier must match the authenticated identifier. Multiple candidates,
conflicting evidence, and invalid evidence stop authentication. Missing evidence
also stops authentication unless the compatibility policy below permits it.
Migration updates both identifier fields atomically and revalidates evidence
under the association lock.

Configuration changes
---------------------

Before switching identifiers, configure extra data to save the proposed new
stable field while the old key is still active. Existing users must authenticate
in this configuration, or receive an independently verified administrative
backfill, before their associations contain that evidence. Adding an extra-data
setting does not populate historical rows automatically.

For example, while Google still uses email::

    SOCIAL_AUTH_GOOGLE_OAUTH2_ID_KEY = "email"
    SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [("sub", "sub")]

Then switch the active key and retain the historical key::

    SOCIAL_AUTH_GOOGLE_OAUTH2_ID_KEY = "sub"
    SOCIAL_AUTH_GOOGLE_OAUTH2_LEGACY_ID_KEYS = ["email"]
    SOCIAL_AUTH_GOOGLE_OAUTH2_ALLOW_UNVERIFIED_LEGACY_UID_MIGRATION = False

Configured historical keys supplement the backend's built-in keys, and work
with an explicit current ``ID_KEY``. Custom backends must implement extraction
for their historical keys when identifiers require transformations or scoping.

If an email or username has changed and its old value is no longer returned,
indexed lookup cannot recover the old association. There is no global JSON
search fallback. Use account recovery or an authenticated linking flow.
Presenting a reclaimed mutable identifier with conflicting stored evidence
always fails, including when unverified migration is enabled.

Compatibility policy
--------------------

``ALLOW_UNVERIFIED_LEGACY_UID_MIGRATION`` defaults to enabled only for the
specific built-in transitions marked "Yes" below. It requires the audited
backend class and current built-in key. Custom subclasses, newly added legacy
keys, and other configuration-driven transitions require evidence by default.
Explicitly selecting the same built-in current key retains that transition's
default. Other current keys do not.

The global ``SOCIAL_AUTH_ALLOW_UNVERIFIED_LEGACY_UID_MIGRATION`` setting and its
backend-specific variants override that default. Explicit ``False`` always
requires evidence. Explicit ``True`` permits missing evidence even outside the
audited list, but cannot override conflicting or invalid evidence.

.. warning::

   Allowing missing evidence accepts the risk that a new owner of an old email,
   username, or other mutable identifier can claim its association. The
   compatibility policy preserves that behavior for known historical setups;
   it does not make those migrations safe. Disable it before upgrading if this
   risk is unacceptable.

.. _historical-identifier-audit:

Historical backend audit
------------------------

This table describes default storage declarations in social-core 5.2.0 for the
25 built-in backend variants that now declare historical identifier keys.
Three stored the new identifier directly; Fence and CAS stored ``sub`` under
``id``. The remaining 20 lacked a directly usable stable identifier field.
Stored ID tokens are not decoded as migration evidence. Actual data can differ
because of older releases, custom pipelines, or extra-data configuration.

.. list-table:: Historical transitions and default compatibility allowances
   :header-rows: 1
   :widths: 25 18 18 22 17

   * - Provider
     - Old key
     - Current key
     - Stored evidence
     - Unverified default
   * - ``arcgis``
     - ``username``
     - ``id``
     - Absent
     - Yes
   * - ``azuread-oauth2``
     - ``upn``
     - ``sub``
     - Absent
     - Yes
   * - ``azuread-oauth2-v2``
     - ``upn``
     - ``sub``
     - Absent
     - Yes
   * - ``azuread-v2-tenant-oauth2``
     - ``preferred_username``
     - ``sub``
     - Absent
     - Yes
   * - ``cas``
     - ``username``
     - ``sub``
     - Alias ``id``
     - No
   * - ``cognito``
     - ``username``
     - ``sub``
     - Absent
     - Yes
   * - ``dailymotion``
     - ``username``
     - ``id``
     - ``id``
     - No
   * - ``deezer``
     - ``name``
     - ``id``
     - Absent
     - Yes
   * - ``discourse``
     - ``email``
     - ``external_id``
     - Absent
     - Yes
   * - ``fence``
     - ``username``
     - ``sub``
     - Alias ``id``
     - No
   * - ``google-oauth``
     - ``email``
     - ``id``
     - Absent
     - Yes
   * - ``google-oauth2``
     - ``email``
     - ``sub``
     - Absent
     - Yes
   * - ``google-onetap``
     - ``email``
     - ``sub``
     - Absent
     - Yes
   * - ``google-openidconnect``
     - ``email``
     - ``sub``
     - Absent
     - Yes
   * - ``keycloak``
     - ``username``
     - ``sub``
     - Absent
     - Yes
   * - ``mailru``
     - ``email``
     - ``id``
     - Absent
     - Yes
   * - ``okta-oauth2``
     - ``preferred_username``
     - ``sub``
     - Absent
     - Yes
   * - ``okta-openidconnect``
     - ``preferred_username``
     - ``sub``
     - Absent
     - Yes
   * - ``opensuse``
     - ``nickname``
     - ``identity_url``
     - Absent
     - Yes
   * - ``qiita``
     - ``id``
     - ``permanent_id``
     - ``permanent_id``
     - No
   * - ``scistarter``
     - ``email``
     - ``profile_id``
     - ``profile_id``
     - No
   * - ``trello``
     - ``username``
     - ``id``
     - Absent
     - Yes
   * - ``tumblr``
     - ``name``
     - ``uuid``
     - Absent
     - Yes
   * - ``ubuntu``
     - ``nickname``
     - ``identity_url``
     - Absent
     - Yes
   * - ``yandex-openid``
     - ``email``
     - ``identity_url``
     - Absent
     - Yes

Django historical backfill
--------------------------

The Django data migration records historical keys using frozen pre-v7 defaults.
It changes neither UIDs nor account ownership. Configure
``SOCIAL_AUTH_OLD_ID_KEYS`` before running it if previous settings selected a
different identifier. This includes Google ``USE_UNIQUE_USER_ID`` and Qiita
``IDENTIFIED_BY_PERMANENT_ID``. For example::

    SOCIAL_AUTH_OLD_ID_KEYS = {
        "google-oauth2": "sub",
        "qiita": "permanent_id",
        "custom-provider": "old_subject",
        "trello": None,
    }

Unknown and skipped providers retain empty keys. Authentication considers them
only through indexed UID candidates and the same evidence policy. A historical
key describes how existing associations were created; current settings alone
cannot establish it. See :doc:`django` for deployment order and migration costs.
