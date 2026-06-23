MailChimp
=========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``mailchimp``
     - ``social_core.backends.mailchimp.MailChimpOAuth2``

MailChimp uses OAuth v2 for Authentication, check the `official docs`_.

- Create an app by filling out the form here: `Add App`_

- Fill ``Client ID`` and ``Client Secret`` values in the settings::

        SOCIAL_AUTH_MAILCHIMP_KEY = '<App UID>'
        SOCIAL_AUTH_MAILCHIMP_SECRET = '<App secret>'

- Add the backend to the ``AUTHENTICATION_BACKENDS`` setting::

        AUTHENTICATION_BACKENDS = (
            ...
            'social_core.backends.mailchimp.MailChimpOAuth2',
            ...
        )

- Then you can start using ``{% url social_core:begin 'mailchimp' %}`` in
  your templates

.. _official docs: https://apidocs.mailchimp.com/oauth2/
.. _Add App: https://admin.mailchimp.com/account/oauth2/
