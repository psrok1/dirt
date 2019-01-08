import os

from shlex import quote

import click


QUIET_MODE = False
SHORT_MODE = False
NO_COLOR = False


def bold(arg):
    return click.style(arg or "", bold=True)


def style_status(is_closed):
    return click.style("closed" if is_closed else "opened", fg=("red" if is_closed else "green"), bold=True)


def echo(fmt, order=None, ignore_short=False, err=True, **elements):
    def arg_style(arg):
        arg = arg or ""
        return bold(arg) if not NO_COLOR else arg
    if SHORT_MODE and not ignore_short:
        if elements:
            click.echo(' '.join([arg_style(elements[key]) for key in (order or elements.keys())]))
    else:
        click.echo(fmt.format(**{key: arg_style(val) for key, val in elements.items()}), err=err)


def shell(fmt, raw=False, **elements):
    try:
        os.fdopen(3, "w").write(((fmt.format(**{key: quote(val)
                                                for key, val in elements.items()})) if not raw else fmt)+"\n")
    except OSError:
        error("Shell extensions not enabled")


NOTIFY_SUCCESS = ("green", "+")
NOTIFY_INFO = ("blue", "*")
NOTIFY_WARNING = ("yellow", "!")
NOTIFY_ERROR = ("red", "!")


def notify(level, fmt, order=None, ignore_short=False, **elements):
    color, indicator = level
    fmt = "[{}] ".format(click.style(indicator, fg=color, bold=True)) + fmt
    echo(fmt, order=order, ignore_short=ignore_short, **elements)


def success(fmt, order=None, **elements):
    notify(NOTIFY_SUCCESS, fmt, order=order, **elements)


def info(fmt, **elements):
    notify(NOTIFY_INFO, fmt, ignore_short=True, **elements)


def warning(fmt, **elements):
    notify(NOTIFY_WARNING, fmt, ignore_short=True, **elements)


def error(fmt, **elements):
    notify(NOTIFY_ERROR, fmt, ignore_short=True, **elements)

