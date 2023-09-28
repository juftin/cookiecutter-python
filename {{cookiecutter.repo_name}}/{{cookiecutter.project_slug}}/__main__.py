"""
Command-line interface
"""

from {{ cookiecutter.project_slug }}.cli import cli as main  # pragma: no cover

if __name__ == "__main__":
    main()
