Reddit
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
   * - ``reddit``
     - ``social_core.backends.reddit.RedditOAuth2``

Reddit implements `OAuth2 authentication workflow`_. To enable it, just follow:

- Register an application at `Reddit Preferences Apps`_

- Fill the **Consumer Key** and **Consumer Secret** values in your settings::

    SOCIAL_AUTH_REDDIT_KEY = ''
    SOCIAL_AUTH_REDDIT_SECRET = ''

- By default the token is not permanent, it will last an hour. To get
  a refresh token just define::

    SOCIAL_AUTH_REDDIT_AUTH_EXTRA_ARGUMENTS = {'duration': 'permanent'}

  This will store the ``refresh_token`` in ``UserSocialAuth.extra_data``
  attribute, to refresh the access token just do::

    from social_django.utils import load_strategy

    strategy = load_strategy(backend='reddit')
    user = User.objects.get(pk=foo)
    social = user.social_auth.filter(provider='reddit')[0]
    social.refresh_token(strategy=strategy,
                         redirect_uri='http://localhost:8000/complete/reddit/')

  Reddit requires ``redirect_uri`` when refreshing the token and it must be the
  same value used during the auth process.

.. _Reddit Preferences Apps: https://ssl.reddit.com/prefs/apps/
.. _OAuth2 authentication workflow: https://github.com/reddit/reddit/wiki/OAuth2
