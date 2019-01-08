import click

from dirt import attributes, hooks

from dirt.libs import incident, log
from dirt.libs import extensions, complete


def custom_attribute(ctx, name):
    @click.command(name, help="Custom attribute {}".format(name))
    @click.argument("value")
    @click.option("--as-list", "-alist", is_flag=True, default=False)
    @click.option("--as-set", "-aset", is_flag=True, default=False)
    def custom_attribute_handler(value, as_list, as_set):
        current = ctx.obj["INCIDENT"]
        if as_list:
            current.add_meta(name, value, type=list)
        elif as_set:
            current.add_meta(name, value, type=set)
        else:
            current.add_meta(name, value)

        current.store()
        log.success("Added {value} to custom attribute {name}", value=value, name=name)
    return custom_attribute_handler


@click.group("add", help="Add attribute (indicator) to incident", cls=extensions.extendable_group(custom_attribute))
@click.option("--incident_id", "-i", default="current", autocompletion=complete.get_completer(complete.incident_list))
@click.option("--force", "-f", is_flag=True, default=False)
@click.pass_context
@hooks.hookable
def add_command(ctx, incident_id, force):
    current = incident.choose_incident(incident_id)
    if current is None:
        log.error("No incident found.")
        ctx.abort()
    if current.closed and not force:
        log.error("Incident is closed - you must open it before adding items (use -f if you don't care).")
        ctx.abort()
    ctx.obj["INCIDENT"] = current


extensions.register_subcommands(add_command,
                                [attributes] + extensions.get_submodule_plugins("attributes"),
                                "ADD_COMMAND")


COMMAND = add_command
