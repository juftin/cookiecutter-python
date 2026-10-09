"""Verify that Copier renders and updates the expected Python project."""

import json
import os
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest
from copier import run_copy, run_update
from jinja2 import UndefinedError


def _git(directory: Path, *args: str) -> None:
    """Run a Git command in a temporary repository used for Copier testing."""
    subprocess.run(
        ["git", *args],
        check=True,
        cwd=directory,
        capture_output=True,
        text=True,
    )


def _commit_all(directory: Path, message: str) -> None:
    """Commit the current files so Copier can calculate a versioned update."""
    _git(directory, "add", ".")
    _git(directory, "commit", "--quiet", "-m", message)


def _initialize_repository(directory: Path) -> None:
    """Initialize a Git repository with deterministic identity for test commits."""
    _git(directory, "init", "--quiet")
    _git(directory, "config", "user.name", "Copier test")
    _git(directory, "config", "user.email", "copier@example.invalid")


@pytest.fixture
def rendered_project(tmp_path: Path) -> Path:
    """Render the template with the answers used by the example project."""
    template_root = Path(__file__).parent.parent
    project_root = tmp_path / "example-project"
    run_copy(
        src_path=str(template_root),
        dst_path=project_root,
        data={
            "build_docker_image": True,
            "publish_to_pypi": True,
            "publish_to_docker_hub": True,
        },
        defaults=True,
        overwrite=True,
        vcs_ref="HEAD",
    )
    return project_root


def test_copier_renders_expected_project(rendered_project: Path) -> None:
    """Keep the generated example project synchronized with the template."""
    expected_project = Path(__file__).parent / "example-project"
    generated_files = {
        path.relative_to(rendered_project)
        for path in rendered_project.rglob("*")
        if path.is_file() and path.name != ".copier-answers.yaml"
    }
    expected_files = {
        path.relative_to(expected_project)
        for path in expected_project.rglob("*")
        if path.is_file() and path.name != ".copier-answers.yaml"
    }

    assert generated_files == expected_files
    for relative_path in generated_files:
        assert (rendered_project / relative_path).read_text() == (
            expected_project / relative_path
        ).read_text()


def test_copier_records_answers(rendered_project: Path) -> None:
    """Ensure generated projects retain the metadata required for updates."""
    answers = (rendered_project / ".github/.copier-answers.yaml").read_text()

    assert "_commit:" in answers
    assert "_src_path:" in answers
    assert "project_name: example-project" in answers
    assert "package_name: example-project" in answers
    assert "user_name: Justin Flannery" in answers
    assert "user_email: juftin@juftin.com" in answers
    assert "github_user: juftin" in answers


def test_copier_defaults_project_name_to_destination_folder(tmp_path: Path) -> None:
    """Use the destination folder name when no project name is supplied."""
    project_root = tmp_path / "folder-named-project"
    run_copy(
        src_path=str(Path(__file__).parent.parent),
        dst_path=project_root,
        defaults=True,
        overwrite=True,
        quiet=True,
        vcs_ref="HEAD",
    )

    answers = (project_root / ".github/.copier-answers.yaml").read_text()
    assert "project_name: folder-named-project" in answers
    assert "package_name: folder-named-project" in answers
    assert (project_root / "src/folder_named_project").is_dir()


def test_copier_allows_custom_package_name(tmp_path: Path) -> None:
    """Use a PyPI-style distribution name while deriving a package slug."""
    project_root = tmp_path / "project-name"
    run_copy(
        src_path=str(Path(__file__).parent.parent),
        dst_path=project_root,
        data={"package_name": "package.name_python"},
        defaults=True,
        overwrite=True,
        quiet=True,
        vcs_ref="HEAD",
    )

    assert (project_root / "src/package_name_python").is_dir()
    assert (
        'name = "package.name_python"' in (project_root / "pyproject.toml").read_text()
    )


@pytest.mark.parametrize(
    ("package_name", "project_slug"),
    [
        ("123-package", "_123_package"),
        ("class", "_class"),
    ],
)
def test_copier_derives_import_safe_package_slug(
    tmp_path: Path,
    package_name: str,
    project_slug: str,
) -> None:
    """Preserve valid PyPI names while generating an import-safe package slug."""
    project_root = tmp_path / "project-name"
    run_copy(
        src_path=str(Path(__file__).parent.parent),
        dst_path=project_root,
        data={"package_name": package_name},
        defaults=True,
        overwrite=True,
        quiet=True,
        vcs_ref="HEAD",
    )

    assert (project_root / f"src/{project_slug}").is_dir()
    assert (
        f"from {project_slug}.__about__ import"
        in (project_root / f"src/{project_slug}/__init__.py").read_text()
    )


def test_copier_omits_disabled_optional_files(tmp_path: Path) -> None:
    """Preserve the optional-file behavior previously handled by hooks."""
    project_root = tmp_path / "minimal-project"
    run_copy(
        src_path=str(Path(__file__).parent.parent),
        dst_path=project_root,
        data={
            "build_docker_image": False,
            "publish_to_pypi": False,
            "publish_to_docker_hub": False,
            "license": "UNLICENSED",
        },
        defaults=True,
        overwrite=True,
        vcs_ref="HEAD",
    )

    assert not (project_root / "Dockerfile").exists()
    assert not (project_root / "LICENSE").exists()
    assert not (project_root / ".github/workflows/docker.yaml").exists()
    assert not (project_root / ".github/workflows/publish.yaml").exists()


@pytest.mark.parametrize(
    ("question", "value"),
    [
        ("project_name", "Invalid Name"),
        ("project_name", "invalid_name"),
        ("project_name", "1invalid"),
        ("package_name", "-invalid-name"),
        ("package_name", "invalid-name-"),
        ("package_name", "invalid/name"),
    ],
)
def test_copier_rejects_invalid_identifiers(
    tmp_path: Path,
    question: str,
    value: str,
) -> None:
    """Reject identifiers that would create invalid package or repository paths."""
    with pytest.raises(ValueError, match=f"Validation error for question '{question}'"):
        run_copy(
            src_path=str(Path(__file__).parent.parent),
            dst_path=tmp_path / "invalid-project",
            data={question: value},
            defaults=True,
            overwrite=True,
            quiet=True,
            vcs_ref="HEAD",
        )


def test_copier_fails_for_undefined_template_variables(tmp_path: Path) -> None:
    """Fail generation when a template refers to an undefined answer."""
    source = tmp_path / "template-source"
    shutil.copytree(
        Path(__file__).parent.parent,
        source,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            ".pytest_cache",
            "__pycache__",
            "site",
        ),
    )
    readme = source / "template/README.md"
    readme.write_text(f"{readme.read_text()}\n{{{{ undefined_template_variable }}}}\n")

    with pytest.raises(UndefinedError):
        run_copy(
            src_path=str(source),
            dst_path=tmp_path / "generated-project",
            defaults=True,
            overwrite=True,
            quiet=True,
        )


def test_copier_updates_using_configured_answers_file(tmp_path: Path) -> None:
    """Update a generated project using its answers file outside the root path."""
    source = tmp_path / "template-source"
    shutil.copytree(
        Path(__file__).parent.parent,
        source,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            ".pytest_cache",
            "__pycache__",
            "site",
        ),
    )
    _initialize_repository(source)
    _commit_all(source, "Initial template")
    _git(source, "tag", "v1.0.0")

    project = tmp_path / "generated-project"
    run_copy(
        src_path=str(source),
        dst_path=project,
        defaults=True,
        overwrite=True,
        quiet=True,
        vcs_ref="v1.0.0",
    )
    _initialize_repository(project)
    _commit_all(project, "Initial project")

    readme = source / "template/README.md"
    marker = "<!-- Updated by Copier -->\n"
    readme.write_text(f"{readme.read_text()}\n{marker}")
    _commit_all(source, "Update template README")
    _git(source, "tag", "v1.1.0")

    run_update(
        dst_path=project,
        answers_file=".github/.copier-answers.yaml",
        defaults=True,
        overwrite=True,
        quiet=True,
        vcs_ref="v1.1.0",
    )

    assert marker in (project / "README.md").read_text()


def test_copier_removes_consolidated_ci_workflows(tmp_path: Path) -> None:
    """Delete replaced CI workflows, including downstream customizations."""
    template_root = Path(__file__).parent.parent
    source = tmp_path / "template-source"
    shutil.copytree(
        template_root,
        source,
        ignore=shutil.ignore_patterns(
            ".git",
            ".venv",
            ".pytest_cache",
            "__pycache__",
            "site",
        ),
    )
    workflow_dir = source / "template/.github/workflows"
    (workflow_dir / "ci.yaml").unlink()
    legacy_workflows = {
        "test.yaml": "test.yaml",
        "lint.yaml": "lint.yaml",
        "docker.yaml": "{% if build_docker_image %}docker.yaml{% endif %}",
    }
    for template_path in legacy_workflows.values():
        (workflow_dir / template_path).write_text("name: legacy\n")

    _initialize_repository(source)
    _commit_all(source, "Initial template")
    _git(source, "tag", "v1.0.0")

    project = tmp_path / "generated-project"
    run_copy(
        src_path=str(source),
        dst_path=project,
        data={"build_docker_image": True},
        defaults=True,
        overwrite=True,
        quiet=True,
        vcs_ref="v1.0.0",
    )
    _initialize_repository(project)
    for filename in legacy_workflows:
        workflow = project / ".github/workflows" / filename
        workflow.write_text(f"{workflow.read_text()}# Downstream customization\n")
    _commit_all(project, "Initial project")

    (workflow_dir / "ci.yaml").write_text(
        (template_root / "template/.github/workflows/ci.yaml").read_text()
    )
    for template_path in legacy_workflows.values():
        (workflow_dir / template_path).unlink()
    _commit_all(source, "Consolidate CI workflows")
    _git(source, "tag", "v1.1.0")

    subprocess.run(
        [
            sys.executable,
            "-m",
            "copier",
            "update",
            "--defaults",
            "--answers-file",
            ".github/.copier-answers.yaml",
            str(project),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert (project / ".github/workflows/ci.yaml").is_file()
    for filename in legacy_workflows:
        assert not (project / ".github/workflows" / filename).exists()


@pytest.mark.parametrize(
    ("release_ref", "expected_version"),
    [("", "0.0.0"), ("v1.2.3", "1.2.3"), ("2.0.0-beta.1", "2.0.0b1")],
)
def test_distribution_uses_release_version_without_changing_source(
    rendered_project: Path,
    release_ref: str,
    expected_version: str,
) -> None:
    """Stamp wheel and sdist metadata while preserving source and lock bytes."""
    pyproject = rendered_project / "pyproject.toml"
    assert 'version = "0.0.0"' in pyproject.read_text()
    original_pyproject = pyproject.read_bytes()
    lockfile = rendered_project / "uv.lock"
    lockfile.write_text("version = 1\n")
    original_lockfile = lockfile.read_bytes()

    task_executable = shutil.which("task")
    assert task_executable is not None
    result = subprocess.run(
        [task_executable, "dist"],
        cwd=rendered_project,
        env={**os.environ, "RELEASE_VERSION": release_ref},
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert pyproject.read_bytes() == original_pyproject
    assert lockfile.read_bytes() == original_lockfile
    wheel = next((rendered_project / "dist").glob("*.whl"))
    with zipfile.ZipFile(wheel) as archive:
        metadata_path = next(
            name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
        )
        assert f"Version: {expected_version}\n" in archive.read(metadata_path).decode()
    sdist = next((rendered_project / "dist").glob("*.tar.gz"))
    with tarfile.open(sdist) as archive:
        metadata = next(
            member
            for member in archive.getmembers()
            if member.name.endswith("/PKG-INFO")
        )
        metadata_file = archive.extractfile(metadata)
        assert metadata_file is not None
        assert f"Version: {expected_version}\n" in metadata_file.read().decode()


def test_releases_do_not_commit_version_changes(rendered_project: Path) -> None:
    """Create release artifacts without configuring release process commits."""
    release_config = json.loads((rendered_project / ".releaserc.json").read_text())
    plugins = release_config["plugins"]
    assert "@semantic-release/git" not in [
        plugin[0] if isinstance(plugin, list) else plugin for plugin in plugins
    ]
