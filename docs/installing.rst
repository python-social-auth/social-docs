Installation
============

python-social-auth_ is a very modular library looking to provide the
basic tools to implement social authentication / authorization in
Python projects. For that reason, the project is split in smaller
components that focus on providing a simpler functionality. Some
components are:

* social-auth-core_
  Core library that the rest depends on, this contains the basic
  functionality to establish an authentication/authorization flow with
  the diferent supported providers.

* social-auth-storage-sqlalchemy_, social-auth-storage-peewee_, social-auth-storage-mongoengine_
  Different storage solutions that can be reused accross the supported
  frameworks or newer implementations.

* social-auth-app-django_, social-auth-app-django-mongoengine_
  Django framework integration

* social-auth-app-flask_, social-auth-app-flask-sqlalchemy_, social-auth-app-flask-mongoengine_, social-auth-app-flask-peewee_
  Flask framework integration

* social-auth-app-pyramid_
  Pyramid framework integration

* social-auth-app-cherrypy_
  Cherrypy framework integration

* social-auth-app-tornado_
  Tornado framework integration

* social-auth-app-webpy_
  Webpy framework integration


Dependencies
------------

Dependencies are properly defined in the requirements files; the
``setup.py`` script will determine the environment where it's
installed and sort between Python 2 or Python 3 packages if
needed. There are some ``extras`` defined to install the corresponding
dependencies since they are required to build extensions that, unless
used, are undesired.

* OpenIDConnect_ support requires the use of the ``openidconnect`` extra.
* SAML_ support requires the use of the ``saml`` extra.

There's also the ``all`` extra that will install all the extra options.

Several backends demand application registration on their
corresponding sites and other dependencies like SQLAlchemy_ on Flask
and Webpy.


Get a copy
----------

From PyPI_::

    $ pip install social-auth-<component>

Or, grab the relevant repository from GitHub_, then::

    $ cd social-auth-<component>
    $ sudo python setup.py install


Using the ``extras`` options
----------------------------

To enable any of the ``extras`` options to bring the dependencies for
OpenIDConnect_, or SAML_, or both::

  $ pip install "social-auth-core[openidconnect]"
  $ pip install "social-auth-core[saml]"
  $ pip install "social-auth-core[all]"


.. _OpenID: http://openid.net/
.. _OpenIDConnect: http://openid.net/connect/
.. _OAuth: http://oauth.net/
.. _SAML: https://www.onelogin.com/saml
.. _PyPI: https://pypi.org/project/social-auth-core/
.. _GitHub: https://github.com/python-social-auth/
.. _python-openid: http://pypi.org/project/python-openid/
.. _requests-oauthlib: https://requests-oauthlib.readthedocs.org/
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _python-social-auth: https://github.com/python-social-auth
.. _social-auth-core: https://github.com/python-social-auth/social-core
.. _social-auth-storage-sqlalchemy: https://github.com/python-social-auth/social-storage-sqlalchemy
.. _social-auth-storage-peewee: https://github.com/python-social-auth/social-storage-peewee
.. _social-auth-storage-mongoengine: https://github.com/python-social-auth/social-storage-mongoengine
.. _social-auth-app-django: https://github.com/python-social-auth/social-app-django
.. _social-auth-app-django-mongoengine: https://github.com/python-social-auth/social-app-django-mongoengine
.. _social-auth-app-flask: https://github.com/python-social-auth/social-app-flask
.. _social-auth-app-flask-mongoengine: https://github.com/python-social-auth/social-app-flask-mongoengine
.. _social-auth-app-flask-peewee: https://github.com/python-social-auth/social-app-flask-peewee
.. _social-auth-app-flask-sqlalchemy: https://github.com/python-social-auth/social-app-flask-sqlalchemy
.. _social-auth-app-pyramid: https://github.com/python-social-auth/social-app-pyramid
.. _social-auth-app-cherrypy: https://github.com/python-social-auth/social-app-cherrypy
.. _social-auth-app-tornado: https://github.com/python-social-auth/social-app-tornado
.. _social-auth-app-webpy: https://github.com/python-social-auth/social-app-webpy
