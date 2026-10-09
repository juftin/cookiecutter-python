# Contributing

## Environment Setup

This project requires two core dependencies: **[uv]** (Python package
manager) and **[task]** (task runner). Once both are installed, you can use
`task` to interact with the project for all development workflows.

1. [Install uv](https://docs.astral.sh/uv/getting-started/installation/)

    ```shell
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2. [Install task](https://taskfile.dev/installation/)

    ```shell
    sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
    ```

3. Install the project development environment

    ```shell
    task install
    ```

4. Optionally, activate the virtual environment created by `uv`:

    ```shell
    source .venv/bin/activate
    ```

## Using Task

### Task Cheat Sheet

| Command Description             | Command                     | Notes                                           |
| ------------------------------- | --------------------------- | ----------------------------------------------- |
| List Available Tasks            | `task`                      | Lists tasks in alphanumeric order               |
| Install Project + Dev Dependencies | `task install`           | Installs dependencies and pre-commit hooks      |
| Run Tests                       | `task test`                 | Runs tests with `pytest`                        |
| Run Tests across Python Versions | `task test:matrix`         | Runs tests on Python 3.10 through 3.14          |
| Code Quality Check - Formatting | `task check:format`         | Checks formatting with `ruff`                   |
| Code Quality Check - Linting    | `task check:lint`           | Checks linting with `ruff`                      |
| Code Quality Check - Formatting + Linting | `task check:style` | Runs formatting and linting checks              |
| Code Quality Check - Type Checking | `task check:types`       | Checks types with `mypy`                        |
| Code Quality Check - Formatting + Linting + Type Checking | `task check` | Runs all code checks          |
| Code Quality Auto-Fix - Formatting | `task fmt`               | Formats code with `ruff`                        |
| Code Quality Auto-Fix - Formatting + Linting | `task fix`       | Formats code and applies `ruff` fixes           |
| Build Distribution Artifacts    | `task dist`                 | Builds Python distribution artifacts             |
| Build Docker Image              | `task docker`               | Builds the Docker image when a Dockerfile exists |
| Build Project Artifacts         | `task build`                | Builds distribution artifacts and Docker image   |
| Publish Docker Image            | `task publish`              | Pushes the Docker image in CI                    |
| Run Documentation Site          | `task docs`                 | Runs MkDocs                                      |
| Run Project Command             | `task run -- <cmd>`         | Runs a command in the project environment        |
| Run Docker Command              | `task docker-run -- <cmd>`  | Runs a command in the Docker image               |
| Regenerate Project Lockfile     | `task lock`                 | Regenerates `uv.lock`                            |

### Task Explanation

`task` is a task runner built in Go that aims to be simpler and easier to use than GNU Make.
Task uses a `Taskfile.yaml` file to define tasks and their dependencies. This project
uses Task to organize and run common development operations like testing, linting,
building, and documentation generation.

To see all available tasks, simply run:

```bash exec="on" result="markdown" source="tabbed-left" tabs="task CLI|Output"
task --list-all
```

To run a specific task, use:

```bash
task test
```

For tasks that need additional arguments, use `--` to pass them:

```bash
task run -- python --version
```

You can also run tasks from subdirectories, and Task will automatically
find and use the `Taskfile.yaml` from the project root.

## Committing Code

This project uses [pre-commit] to run a set of
checks on the code before it is committed. You can install the pre-commit
hooks manually, or they will be set up when you run `task install`.

This project uses [semantic-versioning] standards, managed by [semantic-release].

The source version stays at `0.0.0`. Releases create tags and artifacts without
committing version changes. Package and Docker builds use `RELEASE_VERSION` from
the release tag (with an optional `v` prefix); local builds default to `0.0.0`.
For example, `RELEASE_VERSION=v1.2.3 task build` builds version `1.2.3`.
Package builds reset the source version to `0.0.0` after building and leave
`uv.lock` unchanged. Docker applies the version inside the image.

Releases for this project are handled entirely by CI/CD via pull requests being
merged into the `main` branch. Contributions follow the [gitmoji] standards
with [conventional commits].

While you can denote other changes on your commit messages with [gitmoji], the following
commit message emoji prefixes are the only ones to trigger new releases:

| Emoji | Shortcode     | Description                 | Semver |
| ----- | ------------- | --------------------------- | ------ |
| 💥    | `:boom:`      | Introduce breaking changes. | Major  |
| ✨    | `:sparkles:`  | Introduce new features.     | Minor  |
| 🐛    | `:bug:`       | Fix a bug.                  | Patch  |
| 🚑    | `:ambulance:` | Critical hotfix.            | Patch  |
| 🔒    | `:lock:`      | Fix security issues.        | Patch  |

Most features can be squash merged into a single commit on a pull-request.
When merging multiple commits, they will be summarized into a single release.

If you're working on a new feature, your commit message might look like:

```text
✨ New Feature Description
```

Bug fix commits would look like this:

```text
🐛 Bug Fix Description
```

If you're working on a feature that introduces breaking changes, your
commit message might look like:

```text
💥 Breaking Change Description
```

Other commits that don't trigger a release might look like this:

```text
📝 Documentation Update Description
👷 CI/CD Update Description
🧪 Testing Changes Description
🚚 Moving/Renaming Description
⬆️ Dependency Upgrade Description
```

### Pre-Releases

[semantic-release] supports pre-releases. To trigger a pre-release, you
would merge your pull request into an `alpha` or `beta` branch.

### Specific Release Versions

In some cases you need more advanced control around what kind of release you
need to create. If you need to release a specific version, you can do so by creating a
new branch with the version number as the branch name. For example, if the
current version is `2.3.2`, but you need to release a fix as `1.2.5`, you
would create a branch named `1.2.x` and merge your changes into that branch.

See the [semantic-release documentation] for more information about
branch based releases and other advanced release cases.

[conventional commits]: https://www.conventionalcommits.org/en/v1.0.0/
[gitmoji]: https://gitmoji.dev/
[pre-commit]: https://pre-commit.com/
[semantic-release]: https://github.com/semantic-release/semantic-release
[semantic-release documentation]: https://semantic-release.gitbook.io/semantic-release/usage/configuration#branches
[semantic-versioning]: https://semver.org/
[task]: https://github.com/go-task/task
[uv]: https://github.com/astral-sh/uv
