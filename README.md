<div style="text-align: center;">
  <h1 style="font-size: 36px; margin-top: 0;" align="center">
    cookiecutter-python
  </h1>
  <p style="margin-bottom: 0;" align="center">
    <img src="https://i.imgur.com/g8yxsTP.png" width="400">
  </p>
</div>

[juftin]'s personal [cookiecutter] template for Python projects.

```shell
cookiecutter gh:juftin/cookiecutter-python
```

## Features

-   [hatch] for managing the project's virtual environment and development tools
-   [ruff] for code formatting and linting
-   [mypy] for type checking
-   [pip-tools] for dependency management + lockfile
-   [pre-commit] for managing git hooks
-   [GitHub Actions] for CI/CD
-   [MkDocs] and [mkdocs-material] for documentation
-   [GitHub Pages] for hosting documentation
-   [semantic-release] and [gitmoji] for automated releases
-   Publishes to [PyPI] and [Docker Hub]

## Quickstart Guide

### Requirements

Install [cookiecutter]:

```shell
pipx install cookiecutter
```

[pipx] is preferred, but you can also install with `pip install --user`.

### Creating a project

#### Cookiecutter

Generate a Python project:

```shell
cookiecutter gh:juftin/cookiecutter-python
```

#### Git Init

Change to the root directory of your new project, create a Git
repository, and install [pre-commit]

```shell
git init
pre-commit install
git add .
pre-commit run --all-files
git add .
git commit
```

#### Secrets Init

This project uses GitHub Actions to deploy releases, documentation, and
to publish artifacts to PyPI / Docker Hub. You will need to create
secrets in your GitHub repository to enable these features.

-   `PERSONAL_ACCESS_TOKEN`: A GitHub Personal Access Token with `repo` permissions
-   `PYPI_TOKEN`: Your PyPI token (optional)
-   `DOCKER_USERNAME`: Your Docker Hub username (optional)
-   `DOCKER_TOKEN`: Your Docker Hub token (optional)

#### Developing

This project generates its own documentation for how to use the
project's tools. To view the documentation locally, run:

```shell
hatch run docs:serve
```

Once the server is running, you can view the documentation at
[localhost:8080/contributing] or see a preview at [juftin.com/cookiecutter-python/contributing].

[pre-commit]: https://pre-commit.com/
[gitmoji]: https://gitmoji.dev/
[semantic-release]: https://github.com/semantic-release/semantic-release
[Cookiecutter]: https://github.com/cookiecutter/cookiecutter
[hatch]: https://hatch.pypa.io/latest/
[MkDocs]: https://www.mkdocs.org/
[mkdocs-material]: https://squidfunk.github.io/mkdocs-material/
[Github Actions]: https://github.com/features/actions
[Github Pages]: https://pages.github.com/
[juftin]: https://github.com/juftin
[pipx]: https://pypa.github.io/pipx/
[PyPI]: https://pypi.org/
[Docker Hub]: https://hub.docker.com/
[pip-tools]: https://pip-tools.readthedocs.io/en/latest/
[GitHub CLI]: https://cli.github.com/
[localhost:8080/contributing]: http://localhost:8080/contributing
[ruff]: https://docs.astral.sh/ruff/
[mypy]: https://mypy.readthedocs.io/
[juftin.com/cookiecutter-python/contributing]: https://juftin.com/cookiecutter-python/contributing/
