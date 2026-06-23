ArcGIS
======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``arcgis``
     - ``social_core.backends.arcgis.ArcGISOAuth2``

ArcGIS uses OAuth2 for authentication.

- Register a new application at `ArcGIS Developer Center`_.


OAuth2
------

1. Add the OAuth2 backend to your settings page::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.arcgis.ArcGISOAuth2',
        ...
    )

2. Fill ``Client Id`` and ``Client Secret`` values in the settings::

    SOCIAL_AUTH_ARCGIS_KEY = ''
    SOCIAL_AUTH_ARCGIS_SECRET = ''

.. _ArcGIS Developer Center: https://developers.arcgis.com/
