"""
CookieCutter Tests
"""

import pathlib
import shutil

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture
def cookiecutter_dir() -> pathlib.Path:
    """
    CookieCutter Tests
    """
    _this_file = pathlib.Path(__file__).resolve()
    cookiecutter_dir = _this_file.parent.parent
    test_dir = cookiecutter_dir / "tests"
    output_dir = test_dir / "output"
    output_repo = output_dir / "example-project"
    shutil.rmtree(output_dir, ignore_errors=True)
    cookiecutter(
        template=str(cookiecutter_dir),
        output_dir=str(output_dir),
        no_input=True,
        extra_context={
            "build_docker_image": True,
            "publish_to_pypi": True,
            "publish_to_docker_hub": True,
        }
    )
    return output_repo


def test_cookiecutter_dir(cookiecutter_dir: pathlib.Path) -> None:
    """
    Test file content equality
    """
    all_generated_files = list(cookiecutter_dir.rglob("*"))
    test_files = pathlib.Path(__file__).parent / "example-project"
    file_counter = 0
    for generated_file in all_generated_files:
        relative_path = generated_file.relative_to(cookiecutter_dir)
        test_path = test_files / relative_path
        if generated_file.is_file():
            assert test_path.exists()
            expected = test_path.read_text()
            actual = generated_file.read_text()
            try:
                assert expected == actual
            except AssertionError as e:
                msg = f"Unexpected File Difference - {test_path} - {generated_file}"
                raise ValueError(msg) from e
            file_counter += 1
    assert file_counter > 0


def test_same_files(cookiecutter_dir: pathlib.Path) -> None:
    """
    Test file name / number equality
    """
    test_dir = pathlib.Path(__file__).parent / "example-project"
    all_generated_files = set(f.relative_to(cookiecutter_dir) for f in cookiecutter_dir.rglob("*"))
    all_test_files = set(f.relative_to(test_dir) for f in test_dir.rglob("*"))
    assert all_generated_files == all_test_files
