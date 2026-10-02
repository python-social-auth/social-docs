VK.com (former Vkontakte)
=========================

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``vk-id``
     - ``social_core.backends.vk.VKIDOAuth2``
   * - ``vk-oauth2``
     - ``social_core.backends.vk.VKOAuth2``
   * - ``vk-app``
     - ``social_core.backends.vk.VKAppOAuth2``
   * - ``vk-openapi``
     - ``social_core.backends.vk.VKontakteOpenAPI``

Use VK ID for applications registered with VK ID. The other backends support
legacy VK integrations. Each backend has a separate provider name and settings;
switching to ``vk-id`` does not migrate or automatically link existing
``vk-oauth2`` account associations.

VK ID
-----

Register an application in the `VK ID application dashboard`_ and configure its
allowed redirect URI to match your application's complete URL, for example
``https://example.com/complete/vk-id/``. Follow the `VK ID integration guide`_
for application registration requirements.

Add the backend to Django's ``AUTHENTICATION_BACKENDS`` and set the application
ID as the key::

    AUTHENTICATION_BACKENDS = [
        # Include your other authentication backends here.
        "social_core.backends.vk.VKIDOAuth2",
    ]
    SOCIAL_AUTH_VK_ID_KEY = "your-application-id"

The backend uses the ``id.vk.ru`` endpoints and requires PKCE with S256. It does
not send a client secret. Keep sessions available between the start and complete
requests so the backend can validate ``state`` and retrieve its code verifier.
Do not disable PKCE or select the ``plain`` challenge method.

Start authentication using a POST form::

    <form method="post" action="{% url 'social:begin' 'vk-id' %}">
        {% csrf_token %}
        <button type="submit">Sign in with VK ID</button>
    </form>

Request optional permissions using space-separated OAuth scopes::

    SOCIAL_AUTH_VK_ID_SCOPE = ["email"]

The callback must supply nonempty ``code``, ``device_id``, and ``state`` values.
Both flat query parameters and a JSON object in the ``payload`` parameter are
supported. If both formats supply the same authentication field, their values
must agree. The callback must belong to an authorization started by this backend;
an independently initiated browser SDK flow will not have its session verifier.

The backend retrieves user information server-side and stores the access token,
refresh token, expiry, scope, device ID, and available ID token in ``extra_data``.
Authentication uses the server-provided user ID. An ID token is stored as token
metadata; it is not used as a verified identity claim.

VK ID does not provide a legacy ``screen_name``. The normal pipeline generates
a username unless configured otherwise, for example::

    SOCIAL_AUTH_VK_ID_USERNAME_IS_FULL_EMAIL = True

Refresh tokens
~~~~~~~~~~~~~~

The backend stores the device ID and the registered redirect URI used during
authorization alongside the tokens. The account's ``get_access_token()`` method
automatically refreshes expired tokens using these saved values::

    access_token = social.get_access_token(strategy)

To refresh explicitly and persist rotated tokens, use::

    social.refresh_token(strategy)

Explicit arguments override the saved values when needed::

    social.refresh_token(
        strategy,
        device_id=social.extra_data["device_id"],
        redirect_uri="https://example.com/complete/vk-id/",
    )

Refresh requests include a new state value, which is checked against the
response. Refresh fails if no device ID is available. Direct calls to
``backend.refresh_token()`` must supply the device ID and the registered redirect
URI because they do not have access to the account's saved credentials.

Legacy OAuth2
-------------

For an existing VK OAuth2 application, add
``social_core.backends.vk.VKOAuth2`` to ``AUTHENTICATION_BACKENDS`` and configure::

    SOCIAL_AUTH_VK_OAUTH2_KEY = "your-application-id"
    SOCIAL_AUTH_VK_OAUTH2_SECRET = "your-application-secret"

Start authentication using a POST form::

    <form method="post" action="{% url 'social:begin' 'vk-oauth2' %}">
        {% csrf_token %}
        <button type="submit">Sign in with VK</button>
    </form>

Optional permissions and the API version can be configured with::

    SOCIAL_AUTH_VK_OAUTH2_SCOPE = [...]
    SOCIAL_AUTH_VK_OAUTH2_API_VERSION = "5.131"

See the `VK API access rights`_.

Extra profile data
~~~~~~~~~~~~~~~~~~

The backend requests additional profile fields named in ``EXTRA_DATA``. Entries
can be field names, aliases, or aliases with a flag to discard empty values::

    SOCIAL_AUTH_VK_OAUTH2_EXTRA_DATA = [
        ("screen_name", "display_name"),
        ("photo_50", "avatar"),
        ("nickname", "nickname", True),
    ]

Here ``screen_name`` is the source field requested from VK and ``display_name``
is the key saved in the account's ``extra_data``. Alias names and discard flags
are not sent as API fields. See the `VK API users.get documentation`_ for
available fields.

The backend requests ``photo_50`` for the default avatar. Its URL is also
available as ``photo`` and ``user_photo`` in the profile response for backward
compatibility. Existing ``EXTRA_DATA`` entries using either legacy name request
``photo_50`` and continue to save the same keys.

Legacy application OAuth2
-------------------------

For a VK iframe application, add ``social_core.backends.vk.VKAppOAuth2`` to
``AUTHENTICATION_BACKENDS`` and configure::

    SOCIAL_AUTH_VK_APP_KEY = "your-application-id"
    SOCIAL_AUTH_VK_APP_SECRET = "your-application-secret"

Set the iframe URL to your application's complete URL, for example
``https://example.com/complete/vk-app/``. The callback requires ``is_app_user``,
``viewer_id``, ``access_token``, ``api_id``, and a valid ``auth_key``. The backend
verifies the signature, retrieves the profile directly from VK, and checks that
its user ID matches ``viewer_id``. There is no need to configure an initial
``getProfiles`` request or supply ``api_result``; browser-supplied profile data
is ignored.

Configure the application membership check with::

    SOCIAL_AUTH_VK_APP_USERMODE = 2

``1`` checks the callback's ``is_app_user`` value. ``2`` requests membership
from VK using a signed ``isAppUser`` call and rejects authentication when
membership cannot be confirmed. Omit the setting to skip the membership check;
``0`` does not disable it.

If using the legacy iframe JavaScript SDK, load it over HTTPS::

    <script src="https://vk.com/js/api/xd_connection.js?2"></script>

Serve the iframe application through the HTTPS URL registered with VK.

Legacy OpenAPI
--------------

Add ``social_core.backends.vk.VKontakteOpenAPI`` to
``AUTHENTICATION_BACKENDS`` and configure::

    SOCIAL_AUTH_VK_OPENAPI_APP_ID = "your-application-id"
    SOCIAL_AUTH_VK_OPENAPI_SECRET = "your-application-secret"

The application ID is passed to the local authentication template as
``VK_APP_ID``. Load the legacy OpenAPI SDK over HTTPS::

    <script src="https://vk.com/js/api/openapi.js"></script>

Before completing authentication, your integration must place VK's signed
session cookie value in the strategy session under ``vk_app_<application-id>``.
The backend reads it with ``strategy.session_get()``, checks the signature
against the application secret, and verifies that it has not expired. A browser
cookie alone is insufficient unless your integration makes it available there.

The complete request must also contain ``id``. The authenticated identity comes
from ``mid`` in the verified session, regardless of the request's ``id`` value.
See the `VK OpenAPI authorization documentation`_ for the signed session format.

.. _VK ID application dashboard: https://id.vk.ru/account/
.. _VK ID integration guide: https://id.vk.ru/about/business/go/docs/ru/vkid/latest/vk-id/connection/start-integration/auth-without-sdk/auth-without-sdk-web
.. _VK API access rights: https://dev.vk.com/en/reference/access-rights
.. _VK API users.get documentation: https://dev.vk.com/en/method/users.get
.. _VK OpenAPI authorization documentation: https://dev.vk.com/en/api/open-api/getting-started
