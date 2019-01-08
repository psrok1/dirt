import click

from dirt.libs import incident, log, complete

from dirt import hooks


@click.command("rel", help="Link with another incident")
@click.argument("related", required=True, autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def meta_add_rel_command(ctx, related):
    current = ctx.obj["INCIDENT"]
    with_inc = incident.choose_incident(related, allow_current=False)
    if with_inc is None:
        log.error("No incident found.")
        ctx.abort()
    if with_inc.uuid == current.uuid:
        log.error("Incidents are the same object - relation can't be added")
        ctx.abort()

    current.add_relation(with_inc)
    with_inc.add_relation(current)

    current.store()
    with_inc.store()

    log.success("Marked {incident} as related with {related}",
                incident=current.identifier,
                related=with_inc.identifier)


@click.command("rel", help="Unlink from another incident")
@click.argument("related", required=True, autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def meta_del_rel_command(ctx, related):
    current = ctx.obj["INCIDENT"]
    with_inc = incident.choose_incident(related, allow_current=False)
    if with_inc is None:
        log.error("No incident found.")
        ctx.abort()

    current.remove_relation(with_inc)
    with_inc.remove_relation(current)

    current.store()
    with_inc.store()

    log.success("Unmarked {incident} as related with {related}",
                incident=current.identifier,
                related=with_inc.identifier)


ADD_COMMAND = meta_add_rel_command
DEL_COMMAND = meta_del_rel_command
