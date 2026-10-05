SUSE
====

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``opensuse``
     - ``social_core.backends.suse.OpenSUSEOpenId``

This section describes how to setup the different services provided by SUSE and openSUSE.


openSUSE OpenID
---------------

openSUSE OpenID works straightforward, not settings are needed. Domains or emails
whitelists can be applied too, check the whitelists_ settings for details.

The backend uses the verified OpenID identity URL for account association.
Associations created by older social-core releases used ``nickname`` and
migrate on the next successful authentication.

.. _whitelists: ../configuration/settings.html#whitelists
