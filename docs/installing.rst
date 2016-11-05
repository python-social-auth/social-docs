Installation
============

Dependencies
------------

Dependencies that **must** be met to use the application:

- OpenId_ support depends on python-openid_

- OAuth_ support depends on requests-oauthlib_

- Several backends demands application registration on their corresponding
  sites and other dependencies like sqlalchemy_ on Flask and Webpy.


Get a copy
----------

From pypi_::

    $ pip install social-auth

Or::

    $ easy_install social-auth

Or clone from github_::

    $ git clone git://github.com/python-social-auth/social-core.git

And add social to ``PYTHONPATH``::

    $ export PYTHONPATH=$PYTHONPATH:$(pwd)/social-core/

Or::

    $ cd social-core
    $ sudo python setup.py install


.. _OpenId: http://openid.net/
.. _OAuth: http://oauth.net/
.. _pypi: http://pypi.python.org/pypi/python-social-auth/
.. _github: https://github.com/python-social-auth/social-core
.. _python-openid: http://pypi.python.org/pypi/python-openid/
.. _requests-oauthlib: https://requests-oauthlib.readthedocs.org/
.. _sqlalchemy: http://www.sqlalchemy.org/
