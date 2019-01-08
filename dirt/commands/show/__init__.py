import click

from dirt.libs import incident, log, utils, complete

from dirt import hooks, extensions

import sys
current_module = sys.modules[__name__]


def format_incident(inc):
    ttyw = utils.get_tty_width()
    ttyw = max(35, min(90, ttyw))
    fmt = "{{is_current:^4s}}{{short_id}}    {{cname:{}.{}s}}{{status}}{{tags}}".format(ttyw-24, ttyw-34)
    current = incident.get_current_incident()
    return fmt, {
        "is_current": log.bold(" +  ") if current and current == inc else "    ",
        "cname": inc.cname if inc.cname else "<no description>",
        "status": log.style_status(inc.closed),
        "short_id": inc.identifier[:16],
        "incident": inc.identifier,
        "tags": ("\n" + (" "*24) + " ".join(["#"+tag for tag in inc.tags])) if inc.tags else ""
    }


def format_long_incident(inc):
    return "Incident {incident} ({status})\n\n{cname}\nOwned by {owner}\n\n{attributes}\n{tags}", {
        "status": log.style_status(inc.closed),
        "cname": inc.cname if inc.cname is not None else "No description.",
        "owner": inc.owner,
        "incident": inc.identifier,
        "attributes": utils.pprint_obj({"Attributes": inc.meta}),
        "tags": utils.pprint_obj({"Tags": inc.tags})}


def log_incident(inc):
    fmt, params = format_long_incident(inc)
    log.echo(fmt, order=["incident"], **params)


def log_incidents(incidents):
    for inc in incidents:
        fmt, params = format_incident(inc)
        log.echo(fmt, order=["incident"], **params)


def show_object_attribute(ctx, name):
    @click.command(name, help="Full or partial name of incident or tag")
    def show_object_handler():
        current = incident.choose_incident(name, allow_current=True, multiple=True)
        if current is None:
            incidents = incident.find_incidents_by_tag(name)
            if not incidents:
                log.error("Incident or tag doesn't exist")
                ctx.abort()
            incidents = [incident.choose_incident(inc) for inc in incidents]
            log.echo("Incidents tagged as #{tag}", tag=name)
            log_incidents(incidents)
        elif len(current) == 1:
            log_incident(current[0])
        else:
            log_incidents(current)
    return show_object_handler


@click.group("show",
             help="Show information about incident(s)",
             cls=extensions.extendable_group(show_object_attribute,
                                             completer=complete.get_completer(
                                                 complete.incident_list,
                                                 complete.tags_list)))
@click.pass_context
@hooks.hookable
def show_command(ctx):
    pass


extensions.register_subcommands(show_command, [current_module], "SUBCOMMAND")


COMMAND = show_command
