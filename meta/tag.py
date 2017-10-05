from meta import DirtField
from libs.log import getLogger, bold
import re

log = getLogger()


class TagField(DirtField):
    name = "tag"
    description = "custom queryable tags"

    @classmethod
    def argparser(cls, argp):
        argp = super(TagField, cls).argparser(argp)
        argp.add_argument("value", help="tag to add")
        return argp

    @classmethod
    def add(cls, incident, args):
        tag = args.value.lower()
        p = re.compile(r"^[a-z0-9\_\.]{1,32}$")
        if not p.match(tag):
            log.error("Tag must contain only letters, digits, _ or . chars")
            return False
        cls._add_to_set(incident, "tag", tag)
        log.success("Added tag {}".format(bold("#"+tag)))
        return True

    @classmethod
    def show(cls, incident):
        return ', '.join("#" + tag for tag in incident.meta.get("tag", []))
