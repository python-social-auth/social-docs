Disqus
======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``disqus``
     - ``social_core.backends.disqus.DisqusOAuth2``

Disqus uses OAuth v2 for Authentication.

- Register a new application at the `Disqus API`_, and

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_DISQUS_KEY = ''
      SOCIAL_AUTH_DISQUS_SECRET = ''

- extra scopes can be defined by using::

    SOCIAL_AUTH_DISQUS_AUTH_EXTRA_ARGUMENTS = {'scope': 'likes comments relationships'}

  Check `Disqus Auth API`_ for details.

.. _Disqus Auth API: http://disqus.com/api/docs/auth/
.. _Disqus API: http://disqus.com/api/applications/
