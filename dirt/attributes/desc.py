import click

from dirt.libs import log

from dirt import hooks


@click.command("desc", help="Set incident description")
@click.argument("description", required=True)
@click.pass_context
@hooks.hookable
def meta_add_desc_command(ctx, description):
    current = ctx.obj["INCIDENT"]
    current.cname = description
    current.store()

    log.success("{incident} description set successfully",
                incident=current.identifier)


ADD_COMMAND = meta_add_desc_command
