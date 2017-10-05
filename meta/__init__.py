import pkgutil
from libs.incident import choose_incident
from libs.log import getLogger

log = getLogger()


class DirtField(object):
    name = ""
    description = ""

    @classmethod
    def argparser(cls, argparser):
        argp = argparser.add_parser(cls.name, help=cls.description)
        argp.add_argument("--incident", default=None, help="name of incident (default: current)")
        argp.set_defaults(add=cls._add)
        return argp

    @classmethod
    def _add(cls, args):
        incident = choose_incident(args.incident)
        if incident is None:
            log.error("Cancelled")
            return False
        if incident.closed:
            log.error("Incident is closed - you must open it before adding items.")
            return False
        if cls.add(incident, args):
            incident.store()
        return True

    @classmethod
    def _add_to_set(cls, incident, key, value):
        if key not in incident.meta:
            incident.meta[key] = set()
        incident.meta[key].add(value)

    @classmethod
    def add(cls, incident, args):
        raise NotImplementedError()

    @classmethod
    def show(cls, incident):
        raise NotImplementedError()

# Import all submodules
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    module = loader.find_module(module_name).load_module(module_name)
    exec('%s = module' % module_name)
