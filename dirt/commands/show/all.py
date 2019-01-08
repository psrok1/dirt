import click

from dirt.libs.incident import load_all_incidents
from dirt.commands.show import log_incidents


@click.command("all", help="Shows all incidents")
def show_all_command():
    incidents = list(load_all_incidents())
    log_incidents(incidents)


SUBCOMMAND = show_all_command
