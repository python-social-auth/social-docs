# Agent guidance for social-docs

This repository is the source of the published Python Social Auth documentation
for social-auth-core and its framework integrations. Keep user-facing setup,
configuration, migration, and recovery guidance here.

## Changes and commits

- Match the surrounding reStructuredText style. Use semantic Sphinx references
  for internal pages and document security requirements and upgrade steps when
  behavior changes.
- Write Conventional Commit subjects, such as
  `docs(security): explain identifier recovery`. Add a concise commit body
  explaining why the change is needed. For scanner fixes, include applicable
  finding IDs in the body when available.

## Verification and review handoff

- Run `uvx prek run --all-files` for the configured repository checks.
- After the final edit to documentation source, run a Sphinx build using the
  project's `docs` dependency group. An `AGENTS.md`-only change does not need a
  Sphinx build.
- After amending or rebasing a review branch, rerun checks affected by the
  change. Before calling a pushed branch ready, inspect CI for its latest head
  and report local results separately from CI results. Identify queued, failed,
  or blocked checks explicitly; do not describe them as passed.
