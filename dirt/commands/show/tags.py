import os
import click

from dirt.libs import incident, log, path


@click.command("tags", help="Shows all tags")
@click.pass_context
def show_tags_command(ctx):
    tags = os.listdir(path.get_tags_path())
    if not tags:
        log.error("No tags.")
        ctx.abort()
    log.echo("Known tags")
    for tag in tags:
        log.echo("* {tag}", tag=tag)


SUBCOMMAND = show_tags_command
