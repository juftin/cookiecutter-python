"""
Test cases for the cli.
"""

from click.testing import CliRunner

from example_project.cli import cli


def test_main_succeeds(runner: CliRunner) -> None:
    """
    It exits with a status code of zero.
    """
    result = runner.invoke(cli)
    assert result.exit_code == 0