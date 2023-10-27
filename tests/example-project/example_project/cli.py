"""
example-project: Command Line Interface
"""

import click

from example_project import __application__, __version__


@click.group(invoke_without_command=True)
@click.version_option(version=__version__, prog_name=__application__)
@click.pass_context
def cli(ctx: click.core.Context) -> None:
    """
    Welcome to example-project

    https://github.com/juftin/example-project
    """
    ctx.ensure_object(dict)
    if ctx.invoked_subcommand is None:  # pragma: no cover
        click.echo(ctx.get_help())


if __name__ == "__main__":
    cli()
