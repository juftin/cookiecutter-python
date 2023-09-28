"""
{{ cookiecutter.project_name }}: Command Line Interface
"""

import click

from {{ cookiecutter.project_slug }} import __application__, __version__


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name=__application__)
@click.pass_context
def cli(ctx: click.core.Context) -> None:
    """
    Welcome to {{ cookiecutter.project_name }}

    https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.repo_name }}
    """
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:  # pragma: no cover
        click.echo(ctx.get_help())


if __name__ == "__main__":
    cli()
