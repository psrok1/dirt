from tools import DirtCommand
from libs.incident import choose_incident
from libs.log import getLogger, bold

log = getLogger()


class OpenCommand(DirtCommand):
    command = "open"
    description = "open incident and set as current"

    @classmethod
    def argparser(cls, argp):
        argp = super(OpenCommand, cls).argparser(argp)
        argp.add_argument("incident", nargs="?", default=None, help="incident name (default: current)")
        return argp

    @classmethod
    def execute(cls, args):
        incident = choose_incident(args.incident)
        if incident is None:
            log.error("Cancelled")
            return False
        if not incident.closed:
            log.error("Incident is opened yet")
            return True
        incident.closed = False
        incident.store()
        log.success("Incident {} opened".format(bold(incident.dirname)))
        return True
