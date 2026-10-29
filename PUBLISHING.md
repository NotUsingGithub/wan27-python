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

PyPI allows one pending publisher per owner, repository, workflow, and
environment. The two projects share the workflow file and use different
GitHub environments.

| Field | `wan27` | `langchain-wan27` |
| --- | --- | --- |
| PyPI project name | `wan27` | `langchain-wan27` |
| GitHub owner | `NotUsingGithub` | `NotUsingGithub` |
| Repository | `wan27-python` | `wan27-python` |
| Workflow filename | `publish-pypi.yml` | `publish-pypi.yml` |
| Environment | `pypi` | `pypi-langchain` |

This grants that specific workflow permission to publish these projects. The
PyPI account owner must approve this binding in PyPI. Creating a project through
a pending publisher is subject to PyPI name availability and account limits.

## Validate without publishing

Open Actions → Validate and optionally publish Python packages → Run workflow.
Leave `publish` unchecked. The build job runs; both publish jobs are skipped. The
`python-distributions` artifact contains both wheels and source distributions.

## Publish after the bindings are configured

Run the same workflow on `main` with `publish` checked. The build must pass first.
Two publish jobs then download that artifact, keep only their own distribution
files, and each request a short-lived PyPI identity token. `publish-wan27` uses
the `pypi` environment and uploads `wan27-*` only. `publish-langchain-wan27` uses
the `pypi-langchain` environment and uploads only `langchain_wan27-*`
(the wheel and sdist names produced today) plus `langchain-wan27-*` if a
build emits a hyphenated sdist. Configure required reviewers on those environments if
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
