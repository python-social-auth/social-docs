NGP VAN ActionID
================

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``actionid-openid``
     - ``social_core.backends.ngpvan.ActionIDOpenID``

`NGP VAN`_'s ActionID_ service provides an OpenID 1.1 endpoint, which provides
first name, last name, email address, and phone number.

ActionID doesn't require major settings beside being defined on
``AUTHENTICATION_BACKENDS``

.. code-block:: python

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.ngpvan.ActionIDOpenID',
        ...
    )


If you want to be able to access the "phone" attribute offered by NGP VAN
within ``extra_data`` you can add the following to your settings:

.. code-block:: python

    SOCIAL_AUTH_ACTIONID_OPENID_AX_EXTRA_DATA = [
        ('http://openid.net/schema/contact/phone/business', 'phone')
    ]


NGP VAN offers the ability to have your domain whitelisted, which will disable
the "{domain} is requesting a link to your ActionID" warning when your app
attempts to login using an ActionID account. Contact
`NGP VAN Developer Support`_ for more information

.. _NGP VAN: http://www.ngpvan.com/
.. _ActionID: http://developers.ngpvan.com/action-id
.. _NGP VAN Developer Support: http://developers.ngpvan.com/support/contact
