NFDI (OpenID Connect)
=====================

The NFDI_ backend allows authentication against all OIDC providers of `NFDI`
(German National Research Data Infrastructure) and also for the Helmholtz
AAI. These backends provides their endpoints, as well as the
default scopes.

The provided backends are:

```
XcsOpenIdConnect
TextplusOpenIdConnect
MardiOpenIdConnect
ObjectsOpenIdConnect
CultureOpenIdConnect
CatOpenIdConnect
ChemOpenIdConnect
DatascienceOpenIdConnect
EnergyOpenIdConnect
IngOpenIdConnect
MatWerkOpenIdConnect
DaphneOpenIdConnect
FairmatOpenIdConnect
ImmunoOpenIdConnect
PunchOpenIdConnect
HelmholtzOpenIdConnect
InfraproxyStagingOpenIdConnect
InfraproxyOpenIdConnect
EduidOpenIdConnect
EduidStagingOpenIdConnect
```

A minimum configuration is::

    SOCIAL_AUTH_OIDC_KEY = '<client_id>'
    SOCIAL_AUTH_OIDC_SECRET = '<client_secret>'

The remaining configuration will be auto-detected, by fetching::

    <OIDC_ENDPOINT>/.well-known/openid-configuration

This class can be used standalone, but may also be used as the base class for some other
backends. Find more information at the NFDI_AAI_WEBSITE_

Username
--------

The NFDI_ backend will check for a ``preferred_username`` key in the values
returned by the server.  If the username is under a different key, this can
be overridden::

    SOCIAL_AUTH_OIDC_USERNAME_KEY = 'nickname'

This setting indicates that the username should be populated by the
``nickname`` claim instead.

Scopes
------

The default set of scopes requested are those configured by default in the
cleass. You can request additional claims, for example::

    SOCIAL_AUTH_OIDC_SCOPE = ['groups']


.. _NFDI: https://nfdi.de
.. _NFDI_AAI_WEBSITE: https://doc.nfdi-aai.de
