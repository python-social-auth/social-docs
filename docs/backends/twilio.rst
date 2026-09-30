Twilio Connect
==============

The Twilio backend links a Twilio Connect authorization to an existing local
user. It is not an authentication backend and cannot be used to create users,
sign users in, or recover access to an account.

.. warning::

   The local user must be authenticated before starting the connection. The
   same authenticated user must complete it. Twilio documents Connect as an
   authorization mechanism and recommends placing the Connect button behind
   application authentication.

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``twilio``
     - ``social_core.backends.twilio.TwilioAuth``

Configuration
-------------

- Register a new application using `Twilio Connect`_.

- Fill ``SOCIAL_AUTH_TWILIO_KEY`` and ``SOCIAL_AUTH_TWILIO_SECRET`` in the
  settings::

    SOCIAL_AUTH_TWILIO_KEY = ''
    SOCIAL_AUTH_TWILIO_SECRET = ''

- Add the backend to Django's ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS`` setting::

    'social_core.backends.twilio.TwilioAuth',

Initiating the connection
-------------------------

Framework integrations must pass their current user to
``social_core.actions.do_auth()``. Use an integration release that supports
the authentication initiation hook, or make the equivalent call in a custom
authenticated view::

    do_auth(request.backend, user=request.user)

For Django, initiate the connection with the CSRF-protected POST endpoint while
the local user is signed in::

    <form method="post" action="{% url 'social:begin' 'twilio' %}">
        {% csrf_token %}
        <button type="submit">Connect Twilio</button>
    </form>

The backend binds the callback state to the initiating local user. Anonymous
initiation, anonymous completion, completion by another user, and callback
replay are rejected. A successful callback creates or reuses the ``twilio``
social association for the current user; it does not log that user in again.

Security limitations
--------------------

Twilio returns ``AccountSid`` as a browser-delivered query parameter without a
signature or server-side authorization-code exchange. The backend can prevent
that value from authenticating a local user, but it cannot prove that the
current browser controls the returned Twilio account. An authenticated user
who knows a valid, locally unassociated Connect SID could submit it during
their own association flow.

Treat Connect SIDs as sensitive user data, request only the Twilio permissions
the application needs, and do not use the association as proof of Twilio
account ownership. A Twilio API request can confirm that a SID is currently
usable by the Connect App, but cannot bind it to the browser completing the
flow.

Configure and process Twilio's Deauthorize URL so revoked Connect access also
disables the corresponding local integration.

.. _Twilio Connect: https://www.twilio.com/docs/iam/connect
