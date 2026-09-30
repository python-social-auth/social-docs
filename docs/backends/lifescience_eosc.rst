Lifescience AAI - (Temporary instance for EOSC node)
====================================================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``life_science_eosc``
     - ``social_core.backends.lifescience_eosc.LifeScienceEoscOpenIdConnect``

Lifescience's OpenID Connect (OIDC) backend requires the following minimum
configuration::

    SOCIAL_AUTH_LIFESCIENCE_EOSC_OIDC_KEY = '<client_id>'
    SOCIAL_AUTH_LIFESCIENCE_EOSC_OIDC_SECRET = '<client_secret>'

Scopes
------

The default scopes will include the user's email.
You can request additional claims, for example::

    SOCIAL_AUTH_LIFESCIENCE_EOSC_OIDC_SCOPE = ['eduperson_entitlement']

and you can prevent the inclusion of the default scopes using::

    SOCIAL_AUTH_LIFESCIENCE_EOSC_OIDC_IGNORE_DEFAULT_SCOPE = True
