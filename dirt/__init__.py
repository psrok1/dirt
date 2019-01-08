import click

from dirt import commands

from dirt.commands import shell

from dirt.libs import log, extensions


@click.group(context_settings=dict(help_option_names=['-h', '--help']),
             cls=extensions.passthrough_group(shell.COMMAND))
@click.option("--quiet/--no-quiet", "-q/ ", help="Quiet mode, don't ask for anything", default=False)
@click.option("--short/--no-short", "-s/ ", help="Short mode, print only ids (implies -q and -nc)", default=False)
@click.option("--no-color/--color", "-nc/ ", help="No color in terminal output", default=False)
@click.pass_context
def cli(ctx, quiet, short, no_color):
    """
    Dirty Incident Response Toolkit\n
    psrok1 @ 2017-2019
    """
    log.QUIET_MODE = quiet or short
    log.SHORT_MODE = short
    log.NO_COLOR = no_color or short
    pass


# Import all submodules
extensions.register_subcommands(cli, [commands] + extensions.get_submodule_plugins("commands"), "COMMAND")


def main():
    cli(obj={})


if __name__ == "__main__":
    main()
