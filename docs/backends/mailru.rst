Mail.ru OAuth
=============

Mail.ru uses OAuth2 workflow. `Register new application`_ to use it and fill in settings::

    SOCIAL_AUTH_MAILRU_KEY = ''
    SOCIAL_AUTH_MAILRU_SECRET = ''


Add ``social_core.backends.mailru.MRGOAuth2`` to ``AUTHENTICATION_BACKENDS`` to activate Mail.ru authorization.

Legacy OAuth2 authorization
---------------------------

Also available ``social_core.backends.mailru.MailruOAuth2`` for authorization with ``connect.mail.ru`` server.

`Create an app`_ and set following settings::
    
    SOCIAL_AUTH_MAILRU_OAUTH2_KEY = ''
    SOCIAL_AUTH_MAILRU_OAUTH2_SECRET = ''

.. _Register new application: https://oauth.mail.ru/app/
.. _Create an app: https://api.mail.ru/sites/my/add
