Backends
========

Here's a list and detailed instructions on how to set up the support for each
backend.

Adding new backend support
--------------------------

Add new backends is quite easy, usually adding just a ``class`` with a couple
methods overrides to retrieve user data from services API. Follow the details
in the *Implementation* docs.

.. toctree::
   :maxdepth: 2

   implementation


Supported backends
------------------

Here's the list of currently supported backends.

Non-social backends
*******************

.. toctree::
   :maxdepth: 2

   email
   username

Base OAuth and OpenID classes
*****************************

.. toctree::
   :maxdepth: 2

   oauth
   openid
   saml

Social backends
***************

.. toctree::
   :maxdepth: 2

   amazon
   angel
   apple
   arcgis
   auth0
   auth0_openidconnect
   azuread
   battlenet
   belgium_eid
   bitbucket
   bitbucket_datacenter_oauth2
   box
   bungie
   cas
   cesid
   coinbase
   cognito
   coursera
   dailymotion
   digitalocean
   discogs
   discord
   discourse
   disqus
   douban
   dribbble
   drip
   dropbox
   etsy
   eventbrite
   eveonline
   evernote
   facebook
   facebook_limited_login
   fedora
   fitbit
   flat
   flickr
   foursquare
   github
   github_enterprise
   gitlab
   gitea
   google
   grafana
   helmholtz
   instagram
   justgiving
   kakao
   keycloak
   kick
   lastfm
   launchpad
   lifescience
   lifescience_eosc
   line
   linkedin
   livejournal
   loginradius
   lyft
   mailchimp
   mailru
   mapmyfitness
   mediawiki
   meetup
   mendeley
   microsoftgraph
   mineid
   mixcloud
   nationbuilder
   naver
   nfdi
   odnoklassnikiru
   okta
   openstreetmap_oauth2
   oidc
   orbi
   orcid
   osso
   patreon
   pinterest
   podio
   qiita
   qq
   quizlet
   reddit
   salesforce
   seznam
   shopify
   simplelogin
   sketchfab
   slack
   soundcloud
   spotify
   suse
   stackoverflow
   steam
   stocktwits
   strava
   stripe
   taobao
   telegram
   trello
   tripit
   tumblr
   twilio
   twitch
   twitter
   twitter_oauth2
   udata
   uber
   untappd
   upwork
   vault
   vend
   vimeo
   vk
   weibo
   xing
   yahoo
   yammer
   zotero

Display metadata
----------------

Every shipped backend has a human-readable ``title``. Some also provide an
``icon`` filename referencing social-core's packaged SVG artwork. Applications choose
how to render missing icons. Custom backend classes can declare these attributes::

    class CompanyAuth(OpenIdConnectAuth):
        name = "company"
        title = "Company account"
        icon = None

The display title is independent of the stable ``name`` identifier. Changing
branding does not require renaming stored associations or configuration keys.
Titles are plain strings; applications localize generic labels such as e-mail
or password. See :doc:`/configuration/django` for Django template metadata and
staticfiles integration.
