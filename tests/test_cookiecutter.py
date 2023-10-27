"""
CookieCutter Tests
"""

import pathlib
import tempfile

import pytest
from cookiecutter.main import cookiecutter


@pytest.fixture(scope="session", autouse=True)
def cookiecutter_dir() -> pathlib.Path:
    """
    CookieCutter Tests
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = pathlib.Path(tmpdir)
        _this_file = pathlib.Path(__file__).resolve()
        cookiecutter_dir = _this_file.parent.parent
        cookiecutter(
            template=str(cookiecutter_dir),
            output_dir=str(tmp_path),
            no_input=True,
            extra_context={
                "build_docker_image": True,
                "publish_to_pypi": True,
                "publish_to_docker_hub": True,
            }
        )
        yield tmp_path / "example-project"


def test_cookiecutter_dir(cookiecutter_dir: pathlib.Path) -> None:
    """
    CookieCutter Tests
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
                msg = f"Unexpected File Difference - {test_path}"
                raise ValueError(msg) from e
            file_counter += 1
    assert file_counter > 0
