Testing python-social-auth
============================

The instructions below apply to ``social-auth-core``. Framework integrations
have their own test suites and dependency requirements; follow the contributing
instructions in the integration's repository when changing framework behavior.
See :doc:`development` for working with local checkouts.

The core test suite uses pytest_ and responses_ to mock provider HTTP responses.
Tests do not require live provider accounts, application keys, or secrets. Keep
provider traffic mocked when adding regression tests.

Installing dependencies
-------------------------

From the root of the ``social-core`` checkout, install uv_ and synchronize the
development dependencies and all optional backend dependencies::

    uv sync --all-extras --dev

The SAML dependencies require system libraries, including libxml2 and xmlsec
development packages when building their Python bindings. The core's
`test workflow`_ records the system setup used in CI.

Running tests
---------------

Run the core suite from the checkout root::

    uv run pytest

During development, start with the test module relevant to the change, for
example::

    uv run pytest social_core/tests/backends/test_github.py

Add regression tests for changed behavior. Changes shared by several providers
should cover the common protocol implementation and representative backends.
Changes to framework integration contracts also need tests in the affected
integration repository.

Tox
-----

Use tox_ to test compatibility across the environments configured in the core's
``tox.ini``::

    uvx tox

To select one Python environment, for example Python 3.14::

    uvx tox -e py314

The selected Python interpreters must be available. Consult ``tox.ini`` for the
current environment list.

Linting
---------

Run the repository's configured formatting and linting hooks before submitting
changes::

    uvx prek run --all-files

.. _pytest: https://docs.pytest.org/
.. _responses: https://github.com/getsentry/responses
.. _uv: https://docs.astral.sh/uv/getting-started/installation/
.. _tox: https://tox.wiki/
.. _test workflow: https://github.com/python-social-auth/social-core/blob/master/.github/workflows/test.yml
