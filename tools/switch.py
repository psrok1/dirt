from tools import DirtCommand
from libs.incident import choose_incident, set_current_incident
from libs.log import getLogger, bold

log = getLogger()


class SwitchCommand(DirtCommand):
    command = 'switch'
    description = 'switch to another incident'

    @classmethod
    def argparser(cls, argp):
        argp = super(SwitchCommand, cls).argparser(argp)
        argp.add_argument("incident", help="incident name")
        return argp

    @classmethod
    def execute(cls, args):
        incident = choose_incident(args.incident, allow_current=False)
        if incident is None:
            log.error("Cancelled")
            return False
        set_current_incident(incident)
        log.success("Switched to {}".format(bold(incident.dirname)))
        return True
