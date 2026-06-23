NationBuilder
=============

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``nationbuilder``
     - ``social_core.backends.nationbuilder.NationBuilderOAuth2``

`NationBuilder supports OAuth2`_ as their authentication mechanism. Follow these
steps in order to use it:

- Register a new application at your `Nation Admin panel`_ (define the `Callback
  URL` to ``http://example.com/complete/nationbuilder/`` where ``example.com``
  is your domain).

- Fill the ``Client ID`` and ``Client Secret`` values from the newly created
  application::

    SOCIAL_AUTH_NATIONBUILDER_KEY = ''
    SOCIAL_AUTH_NATIONBUILDER_SECRET = ''

- Also define your NationBuilder slug::

    SOCIAL_AUTH_NATIONBUILDER_SLUG = 'your-nationbuilder-slug'

- Enable the backend in ``AUTHENTICATION_BACKENDS`` setting::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.nationbuilder.NationBuilderOAuth2'
        ...
    )

.. _Nation Admin panel: https://psa.nationbuilder.com/admin/apps
.. _NationBuilder supports OAuth2: http://nationbuilder.com/api_quickstart
