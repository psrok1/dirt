import click

from dirt import attributes, hooks

from dirt.libs import incident, log, complete
from dirt.libs import extensions


def custom_attribute(ctx, name):
    @click.command(name, help="Custom attribute {}".format(name))
    @click.argument("value", required=False, default=None)
    def custom_attribute_handler(value):
        current = ctx.obj["INCIDENT"]
        current.remove_meta(name, value)
        current.store()
        if value is None:
            log.success("Removed custom attribute {name}", name=name)
        else:
            log.success("Removed {value} from custom attribute {name}", value=value, name=name)
    return custom_attribute_handler


@click.group("del", help="Remove attribute (indicator) from incident",
             cls=extensions.extendable_group(custom_attribute))
@click.option("--incident_id", "-i", default="current", autocompletion=complete.get_completer(complete.incident_list))
@click.pass_context
@hooks.hookable
def del_command(ctx, incident_id):
    current = incident.choose_incident(incident_id)
    if current is None:
        log.error("No incident found.")
        ctx.abort()
    if current.closed:
        log.error("Incident is closed - you must open it before adding items.")
        ctx.abort()
    ctx.obj["INCIDENT"] = current


extensions.register_subcommands(del_command,
                                [attributes] + extensions.get_submodule_plugins("attributes"),
                                "DEL_COMMAND")


COMMAND = del_command
