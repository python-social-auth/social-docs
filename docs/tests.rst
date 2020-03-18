Testing python-social-auth
==========================

Testing the application is fairly simple, just met the dependencies and run the
testing suite.

The testing suite uses HTTPretty_ to mock server responses, it's not a live
test against the providers API, to do it that way, a browser and a tool like
Selenium are needed, that's slow, prone to errors on some cases, and some of
the application examples must be running to perform the testing. Plus real Key
and Secret pairs, in the end it's a mess to test functionality which is the
real point.

By mocking the server responses, we can test the backends functionality (and
other areas too) easily and quick.


Installing dependencies
-----------------------

Go to the tests_ directory and install the dependencies listed in the
requirements.txt_. Then run with ``nosetests`` command, or with the
``run_tests.sh`` script.

Tox
---

You can use tox_ to test compatibility against all supported Python versions:

.. code-block:: bash

    $ pip install tox  # if not present
    $ tox


Pending
-------

At the moment only OAuth1, OAuth2 and OpenID backends are being tested, and
just login and partial pipeline features are covered by the test. There's still
a lot to work on, like:

    * Frameworks support

.. _HTTPretty: https://github.com/gabrielfalcao/HTTPretty
.. _tests: https://github.com/python-social-auth/social-core/tree/master/social_core/tests
.. _requirements.txt: https://github.com/python-social-auth/social-core/blob/master/social_core/tests/requirements.txt
.. _tox: http://tox.readthedocs.org/
