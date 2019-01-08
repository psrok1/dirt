import click

from dirt.libs import incident, log, complete

from dirt import hooks


@click.command("close", help="Close incident")
@click.option("--desc", help="Short description of incident (optional)")
@click.argument("incident_id", default="current", autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def close_command(ctx, incident_id, desc):
    current = incident.choose_incident(incident_id)
    if current is None:
        log.error("No incident found.")
        ctx.abort()
    if current.closed:
        log.error("Incident is closed yet")
        ctx.abort()
    if not log.QUIET_MODE and not current.cname and not desc:
        log.warning("Incident doesn't have description. Do you want to add one?")
        desc = click.prompt("Enter description", default="[empty]")
        print(desc)
    if desc:
        current.cname = desc
    current.closed = True
    current.store()
    log.success("Incident {incident} closed", incident=current.identifier)
    ctx.obj["INCIDENT"] = current


COMMAND = close_command
