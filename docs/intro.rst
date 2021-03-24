Introduction
============

Python Social Auth aims to be an easy to setup social authentication and
authorization mechanism for Python projects supporting protocols like OAuth_ (1
and 2), OpenID_ and others.


Features
--------

This application provides user registration and login using social sites
credentials, here are some features, probably not a full list yet.


Supported frameworks
********************

Multiple frameworks support:

    * Django_
    * Flask_
    * Pyramid_
    * Webpy_
    * Tornado_

More frameworks can be added easily (and should be even easier in the future
once the code matures).


Auth providers
**************

Several supported service by simple backends definition (easy to add new ones
or extend current one):

    * Angel_ OAuth2
    * Beats_ OAuth2
    * Behance_ OAuth2
    * Bitbucket_ OAuth1
    * Box_ OAuth2
    * Dailymotion_ OAuth2
    * Deezer_ OAuth2
    * Disqus_ OAuth2
    * Douban_ OAuth1 and OAuth2
    * Dropbox_ OAuth1
    * Eventbrite_ OAuth2
    * Evernote_ OAuth1
    * Facebook_ OAuth2 and OAuth2 for Applications
    * Fitbit_ OAuth2 and OAuth1
    * Flat_ OAuth2
    * Flickr_ OAuth1
    * Foursquare_ OAuth2
    * `Google App Engine`_ Auth
    * GitHub_ OAuth2
    * Google_ OAuth1, OAuth2 and OpenID
    * Instagram_ OAuth2
    * Kakao_ OAuth2
    * Keycloak_ OpenID
    * Linkedin_ OAuth1
    * Live_ OAuth2
    * Livejournal_ OpenID
    * Mailru_ OAuth2
    * MineID_ OAuth2
    * Mixcloud_ OAuth2
    * `Mozilla Persona`_
    * NaszaKlasa_ OAuth2
    * `NGPVAN ActionID`_ OpenID
    * Odnoklassniki_ OAuth2 and Application Auth
    * OpenID_
    * Podio_ OAuth2
    * Pinterest_ OAuth2
    * Rdio_ OAuth1 and OAuth2
    * Readability_ OAuth1
    * Shopify_ OAuth2
    * Skyrock_ OAuth1
    * Soundcloud_ OAuth2
    * Spotify_ OAuth2
    * ThisIsMyJam_ OAuth1
    * Stackoverflow_ OAuth2
    * Steam_ OpenID
    * Stocktwits_ OAuth2
    * Stripe_ OAuth2
    * Tripit_ OAuth1
    * Tumblr_ OAuth1
    * Twilio_ Auth
    * Twitch_ OAuth2
    * Twitter_ OAuth1
    * Upwork_ OAuth1
    * Vimeo_ OAuth1
    * VK.com_ OpenAPI, OAuth2 and OAuth2 for Applications
    * Weibo_ OAuth2
    * Wunderlist_ OAuth2
    * Xing_ OAuth1
    * Yahoo_ OpenID and OAuth1
    * Yammer_ OAuth2
    * Yandex_ OAuth1, OAuth2 and OpenID


User data
*********

Basic user data population, to allow custom fields values from providers
response.


Social accounts association
***************************

Multiple social accounts can be associated to a single user.


Authentication and disconnection processing
*******************************************

Extensible pipeline to handle authentication, association and disconnection
mechanism in ways that suits your project. Check `Authentication Pipeline`_
section.


.. _OpenID: http://openid.net/
.. _OAuth: http://oauth.net/
.. _myOpenID: https://www.myopenid.com/
.. _Angel: https://angel.co
.. _Beats: https://www.beats.com
.. _Behance: https://www.behance.net
.. _Bitbucket: https://bitbucket.org
.. _Box: https://www.box.com
.. _Dailymotion: https://dailymotion.com
.. _Deezer: https://www.deezer.com
.. _Disqus: https://disqus.com
.. _Douban: http://www.douban.com
.. _Dropbox: https://dropbox.com
.. _Eventbrite: https://www.eventbrite.com
.. _Evernote: https://www.evernote.com
.. _Facebook: https://www.facebook.com
.. _Fitbit: https://fitbit.com
.. _Flat: https://flat.io
.. _Flickr: http://www.flickr.com
.. _Foursquare: https://foursquare.com
.. _Google App Engine: https://developers.google.com/appengine/
.. _GitHub: https://github.com
.. _Google: http://google.com
.. _Instagram: https://instagram.com
.. _Kakao: https://kakao.com
.. _Linkedin: https://www.linkedin.com
.. _Live: https://www.live.com
.. _Livejournal: http://livejournal.com
.. _Mailru: https://mail.ru
.. _MineID: https://www.mineid.org
.. _Mixcloud: https://www.mixcloud.com
.. _Mozilla Persona: http://www.mozilla.org/persona/
.. _NaszaKlasa: https://developers.nk.pl/
.. _NGPVAN ActionID: http://developers.ngpvan.com/action-id
.. _Odnoklassniki: http://www.odnoklassniki.ru
.. _Podio: https://podio.com
.. _Shopify: http://shopify.com
.. _Skyrock: https://skyrock.com
.. _Soundcloud: https://soundcloud.com
.. _Spotify: https://www.spotify.com
.. _ThisIsMyJam: https://thisismyjam.com
.. _Stocktwits: https://stocktwits.com
.. _Stripe: https://stripe.com
.. _Tripit: https://www.tripit.com
.. _Twilio: https://www.twilio.com
.. _Twitch: http://www.twitch.tv/
.. _Twitter: http://twitter.com
.. _VK.com: http://vk.com
.. _Weibo: http://weibo.com
.. _Wunderlist: http://wunderlist.com
.. _Xing: https://www.xing.com
.. _Yahoo: http://yahoo.com
.. _Yammer: https://www.yammer.com
.. _Yandex: https://yandex.ru
.. _Pinterest: https://www.pinterest.com
.. _Readability: http://www.readability.com/
.. _Stackoverflow: http://stackoverflow.com/
.. _Steam: http://steamcommunity.com/
.. _Rdio: https://www.rdio.com
.. _Vimeo: https://vimeo.com/
.. _Tumblr: http://www.tumblr.com/
.. _Django: https://github.com/python-social-auth/social-app-django
.. _Flask: https://github.com/python-social-auth/social-app-flask
.. _Pyramid: http://www.pylonsproject.org/projects/pyramid/about
.. _Webpy: https://github.com/python-social-auth/social-app-webpy
.. _Tornado: http://www.tornadoweb.org/
.. _Authentication Pipeline: pipeline.html
.. _Upwork: https://www.upwork.com
