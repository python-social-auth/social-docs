Grafana
=======

Grafana works similar to Facebook (OAuth).

- On your project settings, you should add Grafana on your ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.grafana.GrafanaOAuth2',
    )

- Register a new application at `Grafana Cloud Portal` in grafana.com by doing
  `My Account → SECURITY → OAuth Clients → Add OAuth Client Application`.
  Set any name and in URL just the domain, without any path.

- Copy `client_id` and `client_secret` and add these values in your project settings file.

The ``client_id`` should be added on ``SOCIAL_AUTH_GRAFANA_KEY`` and the ``client_secret`` should be
added on ``SOCIAL_AUTH_GRAFANA_SECRET``::

      SOCIAL_AUTH_GRAFANA_KEY = 'a1b2c3d4'
      SOCIAL_AUTH_GRAFANA_SECRET = 'e5f6g7h8i9'

- The default scope is ```['profile', 'email']``` but it's possible to define it in settings with::

      SOCIAL_AUTH_GRAFANA_SCOPE = [...]
