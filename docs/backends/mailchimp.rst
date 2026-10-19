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

Identity and upgrade behavior
-----------------------------

The backend identifies a connection by the Mailchimp account's ``user_id``
and the authorizing person's ``login.login_id``. Different people with access
to one Mailchimp account therefore have separate local identities. One person
connecting multiple Mailchimp accounts also has a separate association for
each account. The metadata response must contain both identifiers.

Older versions associated users by ``user_id`` alone. On the next sign-in,
an older association is migrated only if its saved ``login.login_id`` matches
the person signing in. If the saved login differs, that person receives a
separate local association. If the saved login identifier is missing, sign-in
stops and the application must use independently verified account recovery or
authenticated account linking. A saved login records the last person who
used an older association, so applications should audit accounts that may
already have been shared before upgrading.

Mailchimp accepts only ``mailchimp_identity`` as its configured ``ID_KEY``.
Before upgrading, remove any ``SOCIAL_AUTH_MAILCHIMP_ID_KEY`` or global
``SOCIAL_AUTH_ID_KEY`` value that selects ``user_id`` or another identifier.
The backend rejects those settings because they can bind different people to
one local account.

.. _official docs: https://apidocs.mailchimp.com/oauth2/
.. _Add App: https://admin.mailchimp.com/account/oauth2/
