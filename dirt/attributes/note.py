import os
import click

from dirt.libs import log

from dirt import hooks


@click.command("note", help="Incident details stored in 'README' file")
@click.pass_context
@hooks.hookable
def meta_note_command(ctx):
    current = ctx.obj["INCIDENT"]
    readme_path = os.path.join(current.dirpath, "README")
    click.edit(filename=readme_path)
    log.success("Note successfully saved in {path}", path=readme_path)


ADD_COMMAND = meta_note_command
