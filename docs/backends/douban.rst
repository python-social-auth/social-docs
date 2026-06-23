Douban
======

Douban supports OAuth2.

Recently Douban launched their OAuth2 support and the new developer site, you
can find documentation at `Douban Developers`_. To setup OAuth2 follow:

- Register a new application at `Create A Douban App`_, make sure to mark the
  **web application** checkbox.

- Fill **Consumer Key** and **Consumer Secret** values in settings::

      SOCIAL_AUTH_DOUBAN_OAUTH2_KEY = ''
      SOCIAL_AUTH_DOUBAN_OAUTH2_SECRET = ''

- Add ``'social_core.backends.douban.DoubanOAuth2'`` into your
  ``SOCIAL_AUTH_AUTHENTICATION_BACKENDS``.

.. _Douban Developers: http://developers.douban.com/
.. _Create A Douban App : http://developers.douban.com/apikey/apply
