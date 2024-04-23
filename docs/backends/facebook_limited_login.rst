Facebook Limited Login
======================

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

.. _Facebook App Creation: https://developers.facebook.com/apps/creation/
.. _Facebook Limited Login: https://developers.facebook.com/docs/facebook-login/limited-login/
.. _hosts file: https://en.wikipedia.org/wiki/Hosts_(file)
