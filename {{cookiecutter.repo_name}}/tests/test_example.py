"""
Example test case for {{ cookiecutter.friendly_name }}.
"""

from {{ cookiecutter.project_slug }} import __application__


def test_example() -> None:
    """
    Just a simple test case.
    """
    assert __application__ == "{{ cookiecutter.friendly_name }}"
