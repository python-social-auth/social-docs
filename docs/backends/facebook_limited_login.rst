Facebook Limited Login
======================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``facebook-limited-login``
     - ``social_core.backends.facebook_limited.FacebookLimitedLogin``

`Facebook Limited Login`_ is required by the Facebook iOS SDK.

App creation
------------

Register a new application at `Facebook App Creation`_, don't use
``localhost`` in the ``App Domains`` and ``Site URL`` fields as
Facebook does not allow this.

Instead, use a placeholder like ``myapp.com`` and define that
domain in your ``/etc/hosts`` or similar file for your OS. For
more information see the `hosts file`_ article on Wikipedia.

Configuration
-------------

Set the ``SOCIAL_AUTH_FACEBOOK_LIMITED_LOGIN_KEY`` to the value
of the ``App Id``.  This field is required for verifying the
Facebook access token received from the iOS SDK.


Django Configuration
--------------------

Set the Facebook Limited Login Key in ``settings.py``:

.. code-block:: python

  SOCIAL_AUTH_FACEBOOK_LIMITED_LOGIN_KEY = "{app_id}"


Enable the auth backend:

.. code-block:: python

  AUTHENTICATION_BACKENDS = (
    ...
    "social_core.backends.facebook_limited.FacebookLimitedLogin",
    ...
  )

Security requirements
---------------------

The client supplies the signed ID token in the ``access_token`` parameter.
The backend verifies the provider signature and applicable issuer, audience,
subject, and time claims. It intentionally does not enforce the token's nonce,
because the backend did not generate it server-side.

Signature validation alone does not bind this token to an authentication
initiated by the receiving browser or make it single-use. Applications requiring
login-CSRF or account-linking replay protection must add an application-level
initiation and single-use binding. Preserve the initiating authenticated local
user through linking; do not treat an arbitrary client nonce as proof of that
binding. See :doc:`../security` for shared deployment requirements.

.. _Facebook App Creation: https://developers.facebook.com/apps/creation/
.. _Facebook Limited Login: https://developers.facebook.com/docs/facebook-login/limited-login/
.. _hosts file: https://en.wikipedia.org/wiki/Hosts_(file)
