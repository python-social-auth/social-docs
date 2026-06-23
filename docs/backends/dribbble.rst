Dribbble
========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``dribbble``
     - ``social_core.backends.dribbble.DribbbleOAuth2``

Dribbble

- Register a new application at Dribbble_, set the callback URL
  to ``http://example.com/complete/dribbble/`` replacing
  ``example.com`` with your domain.

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_DRIBBBLE_KEY = ''
      SOCIAL_AUTH_DRIBBBLE_SECRET = ''

- Also it's possible to define extra permissions with::

      SOCIAL_AUTH_DRIBBBLE_SCOPE = [...]

  See auth scopes at `Dribbble Developer docs`_.


.. _Dribbble: https://dribbble.com/account/applications/new
.. _Dribbble Developer docs: http://developer.dribbble.com/v1/oauth/
