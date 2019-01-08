import click

from dirt.libs import history
from dirt.commands.show import log_incidents


@click.command("history", help="Shows history of processed incidents by user")
def show_history_command():
    incidents = list(history.read_history())
    log_incidents(incidents)


SUBCOMMAND = show_history_command