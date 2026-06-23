Weibo OAuth
===========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``weibo``
     - ``social_core.backends.weibo.WeiboOAuth2``

Weibo OAuth 2.0 workflow.

- Register a new application at Weibo_.

- Fill ``Consumer Key`` and ``Consumer Secret`` values in the settings::

      SOCIAL_AUTH_WEIBO_KEY = ''
      SOCIAL_AUTH_WEIBO_SECRET = ''

By default ``account id``, ``profile_image_url`` and ``gender`` are stored in
extra_data field.

The user name is used by default to build the user instance ``username``,
sometimes this contains non-ASCII characters which might not be desirable for
the website. To avoid this issue it's possible to use the Weibo ``domain``
which will be inside the ASCII range by defining this setting::

    SOCIAL_AUTH_WEIBO_DOMAIN_AS_USERNAME = True

.. _Weibo: http://open.weibo.com
