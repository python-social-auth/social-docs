Development setup
===================

Python Social Auth is split into a framework-independent core and separate
framework integrations and storage packages. The core and Django integration
are actively developed; the other components are in maintenance mode and
welcome maintainers. See the `contributing guide`_ for contribution conventions.

Working on the core
---------------------

Clone the core repository and use uv_ to create its development environment::

    git clone https://github.com/python-social-auth/social-core.git
    cd social-core
    uv sync --all-extras --dev

This installs the local package in editable mode along with its development
and optional backend dependencies. Changes to the checkout are available
without reinstalling it. Optional backends such as SAML may need system
libraries; see :doc:`tests` for dependencies and test commands.

Working on the core and Django together
-----------------------------------------

To develop changes spanning both packages, clone them into sibling directories.
From their parent directory, create a separate environment with both checkouts
installed in editable mode::

    git clone https://github.com/python-social-auth/social-core.git
    git clone https://github.com/python-social-auth/social-app-django.git
    uv venv .venv-social
    uv pip install --python .venv-social/bin/python -e ./social-core -e ./social-app-django

On Windows, use ``.venv-social\Scripts\python.exe`` for the ``--python`` path.
Use this environment's Python to run your application against both local
packages. This shared environment is separate from the repositories' test
environments; follow each repository's instructions to install its test
dependencies and run its suite.

Install only the components needed for your application. Other integrations
can be added as editable checkouts in the same way, subject to their own Python
and dependency requirements.

See :doc:`tests` for core testing and :doc:`releasing` for the core release
process.

.. _contributing guide: https://github.com/python-social-auth/.github/blob/main/CONTRIBUTING.md
.. _uv: https://docs.astral.sh/uv/getting-started/installation/
