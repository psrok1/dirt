import click

from dirt.libs import incident, log, complete

from dirt import hooks


@click.command("open", help="Open incident and set as current")
@click.argument("incident_id", default="current", autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def open_command(ctx, incident_id):
    current = incident.choose_incident(incident_id)
    if current is None:
        log.error("No incident found.")
        ctx.abort()
    if not current.closed:
        log.error("Incident is opened yet")
        ctx.abort()
    current.closed = False
    current.store()
    log.success("Incident {incident} opened", incident=current.identifier)
    ctx.obj["INCIDENT"] = current


COMMAND = open_command
