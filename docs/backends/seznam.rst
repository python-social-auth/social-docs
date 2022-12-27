Seznam
=========

Seznam supports OAuth2 for developers to authenticate users for their apps.
The documentation for the API can be found at `Seznam OAuth documentation`_.
This backend also provides additional configuration options to support
slightly different enterprise versions.

1. Register a new application at `Application management`_, set the
   ``redirect_uri`` to ``http://example.com/complete/seznam-oauth2/``,
   replacing ``example.com`` with your domain.

2. Fill ``client_id`` and ``client_secret`` values in the settings::

    SOCIAL_AUTH_SEZNAM_OAUTH2_KEY = '<client_id>'
    SOCIAL_AUTH_SEZNAM_OAUTH2_SECRET = '<client_secret>'

- If you would like to access some additional information from the user,
    you can set the ``SOCIAL_AUTH_SEZNAM_OAUTH2_SCOPE`` setting to a list
    of extra scopes that are supported according to the `scope documentation`_.
    For example, to request access to the user's phone number and avatar::
    
    SOCIAL_AUTH_SEZNAM_OAUTH2_SCOPE = ['contact-phone', 'avatar']

User ID
-------

Seznam recommends the use of ``oauth_user_id`` as the user identifier instead
of some immutable data as ``username`` or ``email`` because
it can impose security risks if the user changes it.
For that reason ``oauth_user_id`` is used by default, but for compatibility
with the enterprise backed version, you can override this behavior by setting::

    SOCIAL_AUTH_SEZNAM_OAUTH2_ID_KEY = 'id'

.. _Seznam OAuth documentation: https://vyvojari.seznam.cz/oauth/doc?lang=en
.. _Application management: https://vyvojari.seznam.cz/oauth/admin
.. _scope documentation: https://vyvojari.seznam.cz/oauth/scopes?lang=en
