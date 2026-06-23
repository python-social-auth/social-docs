NFDI (OpenID Connect)
=====================

Backend classes
---------------

For Django, choose from these class paths for ``AUTHENTICATION_BACKENDS``.
For other integrations, use the same class paths in the
framework-specific backend setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``helmholtz``
     - ``social_core.backends.nfdi.NFDIOpenIdConnect``
   * - ``xcs``
     - ``social_core.backends.nfdi.XcsOpenIdConnect``
   * - ``textplus``
     - ``social_core.backends.nfdi.TextplusOpenIdConnect``
   * - ``mardi``
     - ``social_core.backends.nfdi.MardiOpenIdConnect``
   * - ``objects``
     - ``social_core.backends.nfdi.ObjectsOpenIdConnect``
   * - ``culture``
     - ``social_core.backends.nfdi.CultureOpenIdConnect``
   * - ``cat``
     - ``social_core.backends.nfdi.CatOpenIdConnect``
   * - ``chem``
     - ``social_core.backends.nfdi.ChemOpenIdConnect``
   * - ``datascience``
     - ``social_core.backends.nfdi.DatascienceOpenIdConnect``
   * - ``energy``
     - ``social_core.backends.nfdi.EnergyOpenIdConnect``
   * - ``ing``
     - ``social_core.backends.nfdi.IngOpenIdConnect``
   * - ``matWerk``
     - ``social_core.backends.nfdi.MatWerkOpenIdConnect``
   * - ``daphne``
     - ``social_core.backends.nfdi.DaphneOpenIdConnect``
   * - ``fairmat``
     - ``social_core.backends.nfdi.FairmatOpenIdConnect``
   * - ``immuno``
     - ``social_core.backends.nfdi.ImmunoOpenIdConnect``
   * - ``punch``
     - ``social_core.backends.nfdi.PunchOpenIdConnect``
   * - ``helmholtz``
     - ``social_core.backends.nfdi.HelmholtzOpenIdConnect``
   * - ``infraproxy-staging``
     - ``social_core.backends.nfdi.InfraproxyStagingOpenIdConnect``
   * - ``infraproxy``
     - ``social_core.backends.nfdi.InfraproxyOpenIdConnect``
   * - ``eduid``
     - ``social_core.backends.nfdi.EduidOpenIdConnect``
   * - ``eduid-staging``
     - ``social_core.backends.nfdi.EduidStagingOpenIdConnect``

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
