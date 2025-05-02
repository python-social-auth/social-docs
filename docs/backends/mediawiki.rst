MediaWiki OAuth1 backend
========================

Usage
-----

In addition to the general setup you need to define the
following settings::

    SOCIAL_AUTH_MEDIAWIKI_KEY = <consumer_key>
    SOCIAL_AUTH_MEDIAWIKI_SECRET = <consumer_secret>
    SOCIAL_AUTH_MEDIAWIKI_URL = 'https://meta.wikimedia.org/w/index.php'

In the OAuth consumer registration you can choose the option to:

    Allow consumer to specify a callback in requests
    and use "callback" URL above as a required prefix

This is preferable. If your URL is `https://myurl.org/` use
the following option::

    SOCIAL_AUTH_MEDIAWIKI_CALLBACK = \
        'https://myurl.org/oauth/complete/mediawiki'

But it is also possible to use::

    SOCIAL_AUTH_MEDIAWIKI_CALLBACK = 'oob'

General documentation
---------------------

https://www.mediawiki.org/wiki/Extension:OAuth

Developer documentation
-----------------------

https://www.mediawiki.org/wiki/OAuth/For_Developers

Code based on
-------------

https://github.com/mediawiki-utilities/python-mwoauth
