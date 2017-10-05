from meta import DirtField
from libs.utils import open_editor
from libs.log import getLogger, bold
import os

log = getLogger()


class NoteField(DirtField):
    name = "note"
    description = "note some details in 'metainfo' file"

    @classmethod
    def add(cls, incident, args):
        fname = incident.dirpath + os.sep + "metainfo"
        if open_editor(fname):
            log.success("Note successfully saved in {}".format(bold(fname)))
        else:
            log.warning("Cancelled.")

    @classmethod
    def show(cls, incident):
        return None
