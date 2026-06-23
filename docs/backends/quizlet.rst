Quizlet
=======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``quizlet``
     - ``social_core.backends.quizlet.QuizletOAuth2``

Quizlet uses OAuth v2 for Authentication.

- Register a new application at the `Quizlet API`_, and

- Add the Quizlet backend to ``AUTHENTICATION_SETTINGS``::

      AUTHENTICATION_SETTINGS = (
        ...
        'social_core.backends.quizlet.QuizletOAuth2',
        ...
      )

- fill ``Client Id`` and ``Client Secret`` values in the settings::

      SOCIAL_AUTH_QUIZLET_KEY = ''
      SOCIAL_AUTH_QUIZLET_SECRET = ''
      SOCIAL_AUTH_QUIZLET_SCOPE = ['read', 'write_set']  # 'write_group' is also available

.. _Quizlet API: https://quizlet.com/api-dashboard
