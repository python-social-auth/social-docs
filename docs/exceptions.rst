.. _authentication-exceptions:

Exceptions
==========

Social Auth exposes structured exceptions so applications can choose recovery
without matching provider descriptions or exception messages.

Catch ``SocialAuthBaseException`` for all Social Auth failures, including
configuration errors. Catch ``AuthException`` for authentication-flow failures.
Both retain their existing inheritance, including ``ValueError``. Configuration
errors inherit directly from ``SocialAuthBaseException``.

Exception families
------------------

``AuthConfigurationError``
    Missing or invalid settings, unavailable backends, or unsupported features.
``AuthInputError``
    Missing or invalid request or application input.
``AuthSessionError``
    Missing authentication context, state mismatch, or a different initiating user.
``AuthResponseError``
    Malformed provider responses or failed signature, claim, nonce, or expiry validation.
``AuthCredentialError``
    Rejected credentials, rejected authorization codes, revoked tokens, or required reauthentication.
``AuthPolicyError``
    Application authentication, membership, or disconnect policy rejection.
``AuthAssociationError``
    Local account conflicts or unsafe identifier migration.
``AuthProviderError``
    Connection, timeout, TLS, rate-limit, availability, or HTTP failures.
``AuthCanceled``
    Explicit authorization cancellation or refusal.
``AuthUnknownError``
    Authentication failures without a known classification.

Structured attributes
---------------------

Each exception exposes ``code``, ``source``, ``stage``, and ``recovery``. Codes
are stable machine-readable strings; messages and diagnostic descriptions are
not part of the classification contract.

``source`` identifies the failing boundary, not who is responsible:
``configuration``, ``request``, ``session``, ``provider_response``,
``local_policy``, ``storage``, or ``unknown``.

``stage`` identifies the operation: ``begin``, ``callback``, ``token_exchange``,
``token_validation``, ``user_info``, ``pipeline``, ``refresh``, ``disconnect``,
or ``unknown``. Custom integrations should supply the stage at the raise site.

``recovery`` suggests an action: ``none``, ``correct_input``, ``restart_login``,
``reauthenticate``, ``retry_later``, ``check_provider_profile``,
``use_existing_account``, or ``contact_administrator``. These hints do not
perform retries or redirects and do not determine whether to report a failure.

Optional attributes are ``backend``, ``parameter``, ``claim``, ``provider_code``,
``status_code``, and ``retry_after``. ``retry_after`` preserves the provider's
HTTP header; applications must interpret it before using it.

``str(exception)`` and ``exception.args`` contain a safe default message.
Provider descriptions are available separately in ``detail``. ``context`` is
an explicitly supplied mapping for diagnostic identifiers, such as user ID and
provider UID. Original exceptions remain available through exception chaining.
Do not send diagnostics, raw responses, or identifying context to client URLs
or flash messages. Do not log tokens, cookies, or full authentication assertions.

``public_metadata()`` returns only ``error_code``, ``error_source``,
``error_stage``, and ``error_recovery``.

.. code-block:: python

    from social_core.exceptions import AuthResponseError, AuthException

    if "sub" not in claims:
        raise AuthResponseError(
            backend, code="missing_claim", claim="sub", stage="token_validation"
        )

    try:
        authenticate()
    except AuthException as error:
        if error.code == "response_expired":
            show_restart_login_message()
        else:
            show_generic_authentication_message()

Application-specific codes should have a namespace, for example
``myapp.registration_disabled``. Explicitly set their source and recovery.
Unknown codes use the family's safe default message and metadata. Never derive
a code from a free-form message.

Reason codes
------------

Defaults are listed below. A raise site can override source or recovery when
its operation supplies more precise information.

.. list-table::
   :header-rows: 1

   * - Code
     - Source
     - Suggested recovery
   * - ``missing_setting``
     - ``configuration``
     - ``contact_administrator``
   * - ``invalid_setting``
     - ``configuration``
     - ``contact_administrator``
   * - ``unsupported_feature``
     - ``configuration``
     - ``contact_administrator``
   * - ``backend_missing``
     - ``configuration``
     - ``contact_administrator``
   * - ``missing_parameter``
     - ``request``
     - ``correct_input``
   * - ``invalid_parameter``
     - ``request``
     - ``correct_input``
   * - ``session_context_missing``
     - ``session``
     - ``restart_login``
   * - ``state_mismatch``
     - ``session``
     - ``restart_login``
   * - ``user_mismatch``
     - ``session``
     - ``restart_login``
   * - ``malformed_response``
     - ``provider_response``
     - ``contact_administrator``
   * - ``missing_claim``
     - ``provider_response``
     - ``contact_administrator``
   * - ``invalid_claim``
     - ``provider_response``
     - ``contact_administrator``
   * - ``invalid_signature``
     - ``provider_response``
     - ``contact_administrator``
   * - ``nonce_mismatch``
     - ``provider_response``
     - ``restart_login``
   * - ``response_expired``
     - ``provider_response``
     - ``restart_login``
   * - ``response_not_yet_valid``
     - ``provider_response``
     - ``contact_administrator``
   * - ``invalid_expiry``
     - ``storage``
     - ``contact_administrator``
   * - ``profile_email_missing``
     - ``provider_response``
     - ``check_provider_profile``
   * - ``authorization_code_rejected``
     - ``provider_response``
     - ``restart_login``
   * - ``credential_rejected``
     - ``provider_response``
     - ``reauthenticate``
   * - ``token_revoked``
     - ``provider_response``
     - ``reauthenticate``
   * - ``reauthentication_required``
     - ``storage``
     - ``reauthenticate``
   * - ``email_verification_rejected``
     - ``request``
     - ``restart_login``
   * - ``authentication_disallowed``
     - ``local_policy``
     - ``contact_administrator``
   * - ``membership_required``
     - ``local_policy``
     - ``contact_administrator``
   * - ``disconnect_disallowed``
     - ``local_policy``
     - ``none``
   * - ``identity_in_use``
     - ``storage``
     - ``use_existing_account``
   * - ``email_in_use``
     - ``storage``
     - ``use_existing_account``
   * - ``username_in_use``
     - ``storage``
     - ``use_existing_account``
   * - ``identifier_migration_conflict``
     - ``storage``
     - ``contact_administrator``
   * - ``connection_failed``
     - ``provider_response``
     - ``retry_later``
   * - ``timeout``
     - ``provider_response``
     - ``retry_later``
   * - ``tls_error``
     - ``provider_response``
     - ``contact_administrator``
   * - ``rate_limited``
     - ``provider_response``
     - ``retry_later``
   * - ``unavailable``
     - ``provider_response``
     - ``retry_later``
   * - ``http_error``
     - ``provider_response``
     - ``contact_administrator``
   * - ``authorization_declined``
     - ``provider_response``
     - ``none``
   * - ``unknown_error``
     - ``unknown``
     - ``contact_administrator``

Provider failures
-----------------

HTTP status alone does not establish cancellation, expired credentials, or a
local policy rejection. Shared HTTP handling retains status and structured
provider codes. Unknown provider codes remain provider errors.

For OAuth, ``invalid_client`` is a configuration failure and ``invalid_grant``
is credential rejection. The latter does not establish expiry. Explicit
``access_denied`` indicates authorization refusal. HTTP 429 and server errors
receive retry-later guidance; TLS verification failures require administrator
attention without suggesting that verification be disabled.

Token renewal failures
----------------------

A stored account with a known expired access token and no usable renewal
credential raises ``AuthCredentialError`` with
``code='reauthentication_required'``, ``source='storage'``, ``stage='refresh'``,
and ``recovery='reauthenticate'``. This applies to explicit ``refresh_token()``
and automatic renewal through ``get_access_token()``. No token request is
sent, and stored credentials remain unchanged. Applications should arrange
another provider login when handling this error. See :ref:`oauth-token-renewal`
for valid tokens, unknown expiry, and backend-specific renewal credentials.

Migration from legacy exceptions
--------------------------------

This is a breaking change. ``SocialAuthBaseException`` and ``AuthException``
remain available for broad catches. ``AuthCanceled`` and ``AuthUnknownError``
also remain available, so catches of these types can be retained. Removed names
have no aliases or wrappers. Update custom backends, pipelines, and catches of
removed types together with the library upgrade.

.. list-table::
   :header-rows: 1

   * - Previous exception
     - Replacement
   * - ``AuthFailed`` / ``AuthTokenError``
     - Choose response, credential, session, policy, or provider failure from the actual cause.
   * - ``AuthMissingParameter`` / ``AuthInvalidParameter``
     - Input errors for request data; configuration errors for settings; response errors for provider fields.
   * - ``AuthStateMissing`` / ``AuthStateForbidden``
     - Session errors with ``session_context_missing`` / ``state_mismatch``.
   * - ``AuthUserMismatch``
     - ``AuthSessionError`` with ``user_mismatch``.
   * - ``AuthTooManyRequests``
     - ``AuthProviderError`` with ``rate_limited``.
   * - ``AuthForbidden``
     - Local policy errors; session errors for user mismatch; provider errors for HTTP rejection.
   * - ``AuthAlreadyAssociated``
     - Association errors with an explicit identity, username, email, or migration-conflict code.
   * - ``AuthTokenRevoked`` / ``AuthReauthenticationRequired``
     - Credential errors with ``token_revoked`` / ``reauthentication_required``.
   * - ``AuthConnectionError`` / ``AuthUnreachableProvider``
     - Provider errors distinguishing connection, timeout, TLS, rate limit, and availability.
   * - ``InvalidEmail``
     - Credential error with ``email_verification_rejected``.
   * - ``NotAllowedToDisconnect``
     - Policy error with ``disconnect_disallowed``.
   * - ``InvalidExpiryValue``
     - Response error with ``invalid_expiry``, source ``storage``, and ``parameter`` identifying the field.
   * - ``WrongBackend`` / ``MissingBackend``
     - Configuration error with ``backend_missing``.
   * - Strategy/configuration errors / ``AuthNotImplementedParameter``
     - Configuration errors with missing/invalid settings or ``unsupported_feature``.

Previously, ``AuthStateMissing`` meant missing session state, while missing
callback state raised ``AuthMissingParameter``. Preserve that distinction when
migrating: use a session error for missing saved state and an input error for a
missing callback parameter.

Construct failures with a backend (or ``None`` where unavailable) and keyword
metadata. Keep provider descriptions in diagnostic positional arguments.
For example, replace ``AuthTokenError(backend, "Signature has expired")`` at a
confirmed expiry boundary with::

    AuthResponseError(
        backend,
        "Signature has expired",
        code="response_expired",
        stage="token_validation",
    )

Do not translate that text into a code elsewhere in the application.
