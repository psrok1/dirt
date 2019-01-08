import click

from dirt.libs import incident, log, path, complete

from dirt import hooks


@click.command("cwd", help="Print incident or tag working dir")
@click.argument("incident_id", default="current", autocompletion=complete.get_completer(complete.incident_list,
                                                                                        complete.tags_list))
@click.pass_context
@hooks.hookable
def cwd_command(ctx, incident_id):
    current = incident.choose_incident(incident_id)
    if current is None:
        tag = incident.get_tag_path(incident_id, create=False)
        if tag is None:
            log.error("Incident or tag doesn't exist")
            ctx.abort()
        tag_path = path.get_tag_path(tag)
        log.success("Tag path: {path}", path=path.get_tag_path(tag))
        ctx.obj["INCIDENT"] = None
        ctx.obj["TAG_PATH"] = tag_path
    else:
        log.success("Incident path: {path}", path=current.dirpath)
        ctx.obj["INCIDENT"] = current


COMMAND = cwd_command
