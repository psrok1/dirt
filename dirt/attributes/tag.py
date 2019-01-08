import click

from dirt.libs import log, complete

from dirt import hooks


@click.command("tag", help="Tags for incident")
@click.argument("tag", required=True, autocompletion=complete.get_completer(complete.tags_list))
@click.pass_context
@hooks.hookable
def meta_add_tag_command(ctx, tag):
    current = ctx.obj["INCIDENT"]
    current.add_tag(tag)
    current.store()
    log.success("Tagged as {tag}", tag="#" + tag)


@click.command("tag", help="Tags for incident")
@click.argument("tag", required=True, autocompletion=complete.get_completer(complete.tags_list))
@click.pass_context
@hooks.hookable
def meta_remove_tag_command(ctx, tag):
    current = ctx.obj["INCIDENT"]
    current.remove_tag(tag)
    current.store()
    log.success("Untagged as {tag}", tag="#" + tag)


ADD_COMMAND = meta_add_tag_command
DEL_COMMAND = meta_remove_tag_command
