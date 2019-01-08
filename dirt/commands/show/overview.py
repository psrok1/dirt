import click

from dirt.libs import incident, log
from dirt.commands.show import log_incidents


@click.command("overview", help="Shows overview")
def show_overview_command():
    incidents = list(incident.load_all_incidents())
    if not log.SHORT_MODE:
        log.echo("Recently opened incidents:")
        log_incidents(list(filter(lambda inc: not inc.closed, incidents))[:5])
    log.echo("Recent incidents:")
    log_incidents(incidents[:5])


SUBCOMMAND = show_overview_command
