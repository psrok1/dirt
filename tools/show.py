from tools import DirtCommand


class ShowCommand(DirtCommand):
    command = 'show'
    description = 'show information about incident(s)'

    @classmethod
    def argparser(cls, argp):
        argp = super(ShowCommand, cls).argparser(argp)
        argp.add_argument("incident", nargs="?", default=None,
                          help="incident name or 'current' or 'all' (default: overview)")
        return argp