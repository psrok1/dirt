from shlex import quote

import click

from dirt import shcmd, hooks

from dirt.libs import log, extensions, incident, complete


def command_arg_completer(ctx, args, incomplete):
    if incomplete == ":":
        incomplete = args[-1] + ":"
    elif args[-1] == ":":
        incomplete = ''.join(args[-2:]) + incomplete
    return complete.incident_expand_arg_list(incomplete)


def custom_command(ctx, name):
    @click.command(name,
                   help="Shell {} command with incident path expansion".format(name),
                   context_settings=dict(
                       ignore_unknown_options=True)
                   )
    @click.argument("args", nargs=-1, type=click.UNPROCESSED,
                    autocompletion=command_arg_completer)
    def custom_shell_command(args):
        try:
            args = [quote(incident.expand_incident_arg(arg)) for arg in args]
        except RuntimeError as e:
            log.error(str(e))
            ctx.abort()
            return
        log.shell(name+' '+(' '.join(args)))
    return custom_shell_command


@click.group("shell",
             cls=extensions.extendable_group(custom_command),
             hidden=True)
@click.pass_context
@hooks.hookable
def shell_command(ctx):
    log.NO_COLOR = True
    pass


extensions.register_subcommands(shell_command, [shcmd] + extensions.get_submodule_plugins("shcmd"), "COMMAND")


COMMAND = shell_command
