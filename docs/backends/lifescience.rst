Lifescience AAI
===============

Lifescience's OpenID Connect (OIDC) backend requires the following minimum
configuration::

    SOCIAL_AUTH_LIFESCIENCE_OIDC_KEY = '<client_id>'
    SOCIAL_AUTH_LIFESCIENCE_OIDC_SECRET = '<client_secret>'

Scopes
------

The default scopes will include the user's email.
You can request additional claims, for example::

    SOCIAL_AUTH_LIFESCIENCE_OIDC_SCOPE = ['eduperson_entitlement']

and you can prevent the inclusion of the default scopes using::

    SOCIAL_AUTH_LIFESCIENCE_OIDC_IGNORE_DEFAULT_SCOPE = True
