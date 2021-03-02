Osso - Open Source SAML SSO
================================

Osso is an open source service that handles SAML tenant onboarding, documentation and authentication.

Your application can then consume normalized user profile resources as part of an OAuth 2.0 authorization code grant flow.

Learn more about Osso at https://ossoapp.com or continue below to start consuming your Osso instance from your application via Python Social Auth.

To enable Osso as a backend:

- On your project settings, add Osso on your ``AUTHENTICATION_BACKENDS``::

    AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.osso.OssoOAuth2',
    )

- Create or update an OAuth Client in your Osso instance, adding a redirect URI to your allow
  ``http://example.com/complete/osso/`` replacing ``http://example.com`` with your application's domain. 
  Grab the ``Client ID`` and ``Client Secret`` to use in your application.

- Add these values of ``Client ID`` and ``Client Secret`` from Osso in your project settings file.

The ``Client ID`` should be added on ``SOCIAL_AUTH_OSSO_KEY`` and the ``Client Secret`` should be
added on ``SOCIAL_AUTH_OSSO_SECRET``. You also need to add your Osso instance base URL as ``SOCIAL_AUTH_OSSO_BASE_URL``::

      SOCIAL_AUTH_OSSO_KEY = os.getenv('SOCIAL_AUTH_OSSO_KEY')
      SOCIAL_AUTH_OSSO_SECRET = os.getenv('SOCIAL_AUTH_OSSO_SECRET')
      SOCIAL_AUTH_OSSO_BASE_URL = 'https://demo.ossoapp.com'
      
When constructing your sign in flow, Osso supports passing an ``email`` or ``domain`` parameter in order to route 
the user to the correct IDP. If you don't include one of these parameters, and instead implement a button, Osso 
will display a hosted login page. Here's an example login form with ``email``:


.. code-block:: html+django

      <form action="{% url 'social:begin' 'osso' %}" method="post" class="login-form">
          <label>Email</label>
          <input type="email" name="email" />
          {% csrf_token %}
          <button type="submit">Sign in with SSO</button>
      </form>  
