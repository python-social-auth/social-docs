Microsoft Graph
===============


1. Go to `Azure portal`_ and create an application. 

2. Fill App Id and Secret in your project settings::

    SOCIAL_AUTH_MICROSOFT_GRAPH_KEY = '...'
    SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET = '...'


3. Enable the backend::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.microsoft.MicrosoftOAuth2',
        ...
    )

`Register an application with the Microsoft identity platform`_.

.. _Azure portal: https://portal.azure.com/
.. _Register an application with the Microsoft identity platform: https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app

