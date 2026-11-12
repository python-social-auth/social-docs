Releasing social-auth-core
============================

This guide describes the ``social-auth-core`` release process implemented by
its `release workflow`_. Other components may use different workflows; check
their repository documentation before releasing them.

Preparing a release
---------------------

1. Update ``project.version`` in ``pyproject.toml`` using the project's
   `Semantic Versioning`_ policy.
2. Review the ``Unreleased`` entries in ``CHANGELOG.md`` and include any missing
   changes. Move the release's entries into a section matching the package
   version, with a release link and date. Leave an empty ``Unreleased`` section
   above it. For example::

       ## [Unreleased]

       ## [7.2.0](https://github.com/python-social-auth/social-core/releases/tag/7.2.0) - 2026-11-12

       ### Added

       - Describe the changes included in this release.

3. Commit the preparation using `Conventional Commits`_, for example
   ``chore: release 7.2.0``, and open a pull request against ``master``. Complete
   the pull request template and request review from the maintainers.
4. Merge the reviewed release pull request after its checks pass.

Pushing the release tag
-------------------------

Create the version tag on the merged release commit and push that tag to the
upstream repository. For example, with ``origin`` pointing to the upstream
``python-social-auth/social-core`` repository::

    git switch master
    git pull --ff-only origin master
    git tag -a 7.2.0 <release-commit-sha> -m "Release 7.2.0"
    git push origin 7.2.0

Replace the example version and ``<release-commit-sha>`` with the intended
version and merged release commit. Verify that the tagged commit contains the
matching package version and a nonempty changelog section. Existing core tags
use the bare version number; the workflow also accepts a leading ``v`` when
looking up changelog notes.

Push the tag first. Do not create or publish a release through GitHub's
``Draft a new release`` interface to start this process. The workflow runs on
tag pushes, and creating a release in advance conflicts with its release
creation step. Publishing an empty immutable release also prevents CI from
adding the distribution assets afterward.

What CI publishes
-------------------

The workflow builds a wheel and source distribution, rebuilds a wheel from the
source distribution, and checks installation, metadata, and distribution
contents. Once these checks pass, two independent jobs publish the artifacts:

* The PyPI job publishes the validated distributions from the upstream
  repository using trusted publishing through the ``pypi`` environment, with
  attestations enabled.
* The GitHub job extracts the tagged version's notes from ``CHANGELOG.md``,
  creates a draft release with the wheel and source distribution attached,
  and then publishes the draft. Uploading all assets before publication
  supports immutable releases.

Monitor the `Release workflow runs`_ and verify that both publishing jobs
complete. Check the version and distributions on PyPI_ and the notes and
assets on `GitHub Releases`_. Success on one service does not imply success
on the other.

Handling a failed publication
-------------------------------

Inspect the failed job and the publication state on both services before
retrying. The GitHub job refuses to overwrite any existing release for the
tag, including a draft. If it left an incomplete draft, inspect and remove
that draft before retrying the failed GitHub job.

A published immutable release cannot have its distribution assets replaced.
Asset corrections require a new version and tag. Do not move the published
tag or try to replace its assets. When retrying a failed job, account for the
other publishing job having already succeeded.

.. _release workflow: https://github.com/python-social-auth/social-core/blob/master/.github/workflows/release.yml
.. _Semantic Versioning: https://semver.org/spec/v2.0.0.html
.. _Conventional Commits: https://www.conventionalcommits.org/
.. _Release workflow runs: https://github.com/python-social-auth/social-core/actions/workflows/release.yml
.. _PyPI: https://pypi.org/project/social-auth-core/
.. _GitHub Releases: https://github.com/python-social-auth/social-core/releases
