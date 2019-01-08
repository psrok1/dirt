import click

from dirt.libs import incident, log, path, complete

from dirt import hooks


@click.command("export", help="Export incident to .tar.gz archive")
@click.argument("incident_id", default="current", autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def shell_export_command(ctx, incident_id):
    current = incident.choose_incident(incident_id)
    if current is None:
        ctx.abort()
    log.shell("tar -zcvf {archive} -C {path} {identifier}",
              archive="dirt-{}.tar.gz".format(current.identifier),
              path=path.get_incidents_path(),
              identifier=current.identifier)


COMMAND = shell_export_command
