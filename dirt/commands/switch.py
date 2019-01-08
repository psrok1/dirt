import click

from dirt.libs import incident, log, complete

from dirt import hooks


@click.command("switch", help="Switch to another incident")
@click.argument("incident_id", default="previous", autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def switch_command(ctx, incident_id):
    current = incident.choose_incident(incident_id, allow_current=False)
    if current is None:
        log.error("No incident found.")
        ctx.abort()
    incident.set_current_incident(current)
    log.success("Switched to {incident}", incident=current.identifier)
    ctx.obj["INCIDENT"] = current


COMMAND = switch_command
