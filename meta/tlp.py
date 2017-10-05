from meta import DirtField
from termcolor import colored
from libs.log import getLogger
from libs.utils import ask

log = getLogger()


class TlpField(DirtField):
    name = "tlp"
    description = "tlp mark"
    TLP_LEVELS = ["white", "green", "yellow", "red"]

    @classmethod
    def argparser(cls, argp):
        argp = super(TlpField, cls).argparser(argp)
        argp.add_argument("value", help="tlp value", choices=TlpField.TLP_LEVELS)
        return argp

    @staticmethod
    def format_tlp(tlp):
        return colored("tlp:"+tlp, tlp, attrs=["bold"])

    @staticmethod
    def is_tlp_lower(new_tlp, current_tlp):
        weight = lambda tlp: TlpField.TLP_LEVELS.index(tlp)
        return weight(new_tlp) > weight(current_tlp)

    @classmethod
    def add(cls, incident, args):
        if "tlp" in incident.meta and cls.is_tlp_lower(incident.meta["tlp"], args.value):
            log.warning("{} is less restrictive than {}.".format(cls.format_tlp(args.value), cls.format_tlp(incident.meta["tlp"])))
            if not ask("Do you really want to set tlp level?"):
                log.info("Cancelled.")
                return False
        incident.meta["tlp"] = args.value
        log.success("Marked as {}".format(cls.format_tlp(args.value)))
        return True

    @classmethod
    def show(cls, incident):
        if "tlp" in incident.meta:
            return TlpField.format_tlp(incident.meta["tlp"])
        else:
            return None
