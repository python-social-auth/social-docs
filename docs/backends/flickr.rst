Flickr
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
   * - ``flickr``
     - ``social_core.backends.flickr.FlickrOAuth``

Flickr uses OAuth v1.0 for authentication.

- Register a new application at the `Flickr App Garden`_, and

- fill ``Key`` and ``Secret`` values in the settings::

      SOCIAL_AUTH_FLICKR_KEY = ''
      SOCIAL_AUTH_FLICKR_SECRET = ''

- Flickr might show a messages saying "Oops! Flickr doesn't recognise the
  permission set.", if encountered with this error, just define this setting::

    SOCIAL_AUTH_FLICKR_AUTH_EXTRA_ARGUMENTS = {'perms': 'read'}


.. _Flickr App Garden: http://www.flickr.com/services/apps/create/
