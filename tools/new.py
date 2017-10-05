from libs.incident import get_current_incident, set_current_incident, Incident
from tools import DirtCommand
from libs.log import getLogger, bold
from libs.utils import ask

log = getLogger()


class NewCommand(DirtCommand):
    command = "new"
    description = "create new incident and set as current"

    @classmethod
    def argparser(cls, argp):
        argp = super(NewCommand, cls).argparser(argp)
        argp.add_argument("--desc", help="short description of incident (optional)")
        return argp

    @classmethod
    def execute(cls, args):
        current = get_current_incident()
        if current is not None and not current.closed:
            log.warning("Current incident {} is opened.".format(bold(current.dirname)))
            if not ask("Do you really want to create new incident"):
                log.info("Cancelled.")
                return False
        incident = Incident(cname=args.desc)
        incident.store()
        set_current_incident(incident)
        log.success("New incident created {}".format(bold(incident.dirname)))
        return True
