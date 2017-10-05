from tools import DirtCommand
from libs.incident import choose_incident
from libs.log import getLogger, bold
from libs.utils import ask_str

log = getLogger()


class CloseCommand(DirtCommand):
    command = "close"
    description = "close incident"

    @classmethod
    def argparser(cls, argp):
        argp = super(CloseCommand, cls).argparser(argp)
        argp.add_argument("incident", nargs="?", default=None, help="incident name (default: current)")
        argp.add_argument("--desc", help="short description of incident (optional)")
        return argp

    @classmethod
    def execute(cls, args):
        incident = choose_incident(args.incident)
        if incident is None:
            log.error("Cancelled")
            return False
        if incident.closed:
            log.error("Incident is closed yet")
            return True
        if not incident.cname and not args.desc:
            log.warning("Incident doesn't have description. Do you want to add one?")
            args.desc = ask_str("[empty]")
        if args.desc:
            incident.cname = args.desc
        incident.closed = True
        incident.store()
        log.success("Incident {} closed".format(bold(incident.dirname)))
        return True
