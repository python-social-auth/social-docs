ORCID
=====

ORCID_ uses OAuth 2 for authentication.

- Register an ORCID account, go to `Developer tools`_, enable the public API,
  create a new application, set the redirect URI to
  ``http://example.com/complete/orcid/`` replacing ``example.com`` with your
  domain.

- Fill the ``Client ID`` and ``Client secret`` values from the app details in
  `Developer tools` (you might need to press "Show details") in the settings::

      SOCIAL_AUTH_ORCID_KEY = ''
      SOCIAL_AUTH_ORCID_SECRET = ''


Member API
----------

You can subscribe to gain access to an `API with extended capabilities`_.
Use ``'social_core.backends.orcid.ORCIDMemberOAuth2'`` class in your
``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.


Sandbox
-------

ORCID supports a sandbox mode for testing, there's a custom backend for it
which name is ``orcid-sandbox`` instead of ``orcid``. Same settings apply
but use these instead::

      SOCIAL_AUTH_ORCID_SANDBOX_KEY = ''
      SOCIAL_AUTH_ORCID_SANDBOX_SECRET = ''

Sandbox is also available for Member API. You will have to register for with
ORCID it `separately`_.

.. _ORCID: https://orcid.org/
.. _Developer tools: https://orcid.org/developer-tools
.. _API with extended capabilities: https://orcid.org/organizations/integrators/API
.. _separately: https://orcid.org/content/register-client-application-sandbox
