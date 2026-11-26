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

LiveJournal OpenID is provided by URLs in the form
``https://<username>.livejournal.com``. This application retrieves the ``username``
from the data in the current
request by checking a parameter named ``openid_lj_user`` which can be sent by
``POST`` or ``GET``.

Some LiveJournal callbacks assert a legacy ``http://`` journal identity. The
backend verifies that identity against the journal's HTTPS discovery document
and keeps the asserted HTTP identifier as the account key.

Journal names can change owner. LiveJournal is therefore available only to
associate a journal with an already authenticated local user; it cannot sign
users in anonymously or create local users. Existing associations remain
available for association management, but applications that used LiveJournal
for login must offer another sign-in method. A user who can no longer sign in
must recover their local account through an independently verified method.
After confirming the current journal owner, an administrator can remove a stale
association from the previous local account; the current owner can then sign
in locally and associate the journal again. Do not transfer an association
solely because a journal name matches.
