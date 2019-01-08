import click

from dirt.libs import incident, log, complete

from dirt import hooks


@click.command("cd", help="Set PWD to incident dir")
@click.argument("incident_id", default="current", autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def shell_cd_command(ctx, incident_id):
    current = incident.choose_incident(incident_id)
    if current is None:
        ctx.abort()
    log.shell("cd {path}", path=current.dirpath)


COMMAND = shell_cd_command
