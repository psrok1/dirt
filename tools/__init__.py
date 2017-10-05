import pkgutil


class DirtCommand(object):
    command = ""
    description = ""

    @classmethod
    def argparser(cls, argparser):
        argp = argparser.add_parser(cls.command, help=cls.description)
        argp.set_defaults(func=cls.execute)
        return argp

    @classmethod
    def execute(cls, args):
        raise NotImplementedError()

# Import all submodules
__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    module = loader.find_module(module_name).load_module(module_name)
    exec('%s = module' % module_name)
