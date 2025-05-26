Fedora
======

Fedora's OpenID Connect (OIDC) backend requires the following minimum
configuration::

    SOCIAL_AUTH_FEDORA_OIDC_KEY = '<client_id>'
    SOCIAL_AUTH_FEDORA_OIDC_SECRET = '<client_secret>'

Scopes
------

The default scopes will include the user's group and agreements.
You can request additional claims, for example::

    SOCIAL_AUTH_FEDORA_OIDC_SCOPE = ['groups']

and you can prevent the inclusion of the default scopes using::

    SOCIAL_AUTH_FEDORA_OIDC_IGNORE_DEFAULT_SCOPE = True


Environment
-----------

You can override the location of the OIDC provider with the
``SOCIAL_AUTH_FEDORA_OIDC_OIDC_ENDPOINT`` setting. For example, to authenticate with
Fedora's staging environment, use this setting::

    SOCIAL_AUTH_FEDORA_OIDC_OIDC_ENDPOINT = 'https://id.stg.fedoraproject.org'
