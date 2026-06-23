LiveJournal
===========

Backend class
-------------

For Django, add this class path to ``AUTHENTICATION_BACKENDS``. For other
integrations, use the same class path in the framework-specific backend
setting.

.. list-table::
   :header-rows: 1

   * - Backend name
     - Class path
   * - ``livejournal``
     - ``social_core.backends.livejournal.LiveJournalOpenId``

LiveJournal provides OpenID, it doesn't require any major settings in order to
work, beside being defined on ``AUTHENTICATION_BACKENDS```::

    SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
        ...
        'social_core.backends.livejournal.LiveJournalOpenId',
        ...
    )

LiveJournal OpenID is provided by URLs in the form ``http://<username>.livejournal.com``,
this application retrieves the ``username`` from the data in the current
request by checking a parameter named ``openid_lj_user`` which can be sent by
``POST`` or ``GET``.
