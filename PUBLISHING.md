# Publish Wan27 Python packages

Both `wan27` and `langchain-wan27` live in this repository. The GitHub workflow
`.github/workflows/publish-pypi.yml` tests, builds, checks and installs both
packages. By default it only validates and produces downloadable distribution
artifacts. It never calls paid Wan27 APIs in its tests.

## One-time PyPI account setup

Sign in to your own PyPI account and complete any account verification and 2FA.
No password or PyPI API token needs to be shared with an assistant or stored in
GitHub. Follow the official pending-publisher documentation:
https://docs.pypi.org/trusted-publishers/creating-a-project-through-oidc/

At https://pypi.org/manage/account/publishing/ add two pending GitHub publishers,
one for each project. If either project already exists under your ownership,
use its project settings to add an existing-project Trusted Publisher instead.

| Field | Value |
| --- | --- |
| PyPI project name | `wan27` for the first entry, `langchain-wan27` for the second |
| GitHub owner | `NotUsingGithub` |
| Repository | `wan27-python` |
| Workflow filename | `publish-pypi.yml` |
| Environment | `pypi` |

This grants that specific workflow permission to publish these projects. The
PyPI account owner must approve this binding in PyPI. Creating a project through
a pending publisher is subject to PyPI name availability and account limits.

## Validate without publishing

Open Actions → Validate and optionally publish Python packages → Run workflow.
Leave `publish` unchecked. The build job runs; the publish job is skipped. The
`python-distributions` artifact contains both wheels and source distributions.

## Publish after the bindings are configured

Run the same workflow on `main` with `publish` checked. The build must pass first;
only the publish job can request a short-lived PyPI identity token. It uses the
`pypi` GitHub environment. Configure required reviewers on that environment if
available for the repository, to add a separate release review.

Verify the actual PyPI versions and project links after publication:

- https://pypi.org/project/wan27/
- https://pypi.org/project/langchain-wan27/

Then install from PyPI in an isolated environment and run import checks. A
successful validation-only workflow is not a successful PyPI publication. If a
publish run partially succeeds, inspect which files actually reached PyPI before
retrying; do not assume both projects were uploaded atomically.

Official publishing mechanism:
https://docs.pypi.org/trusted-publishers/using-a-publisher/
