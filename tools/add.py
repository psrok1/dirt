from tools import DirtCommand
from meta import DirtField


class AddCommand(DirtCommand):
    command = "add"
    description = "add item (indicator) to incident"

    @classmethod
    def argparser(cls, argp):
        argp = super(AddCommand, cls).argparser(argp)
        argfields = argp.add_subparsers(title="supported fields")
        [cls.argparser(argfields) for cls in DirtField.__subclasses__()]
        return argp

    @classmethod
    def execute(cls, args):
        return args.add(args)
