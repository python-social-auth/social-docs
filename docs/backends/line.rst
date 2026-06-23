Line.me
=======

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``line``
     - ``social_core.backends.line.LineOAuth2``

Fill App Id and Secret in your project settings::

	SOCIAL_AUTH_LINE_KEY = '...'
	SOCIAL_AUTH_LINE_SECRET = '...'
