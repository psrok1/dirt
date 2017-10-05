import os
from uuid import uuid4, UUID
from datetime import datetime
from base64 import b32encode, b32decode
from libs.utils import get_username
from config import get_incidents_path, get_current_incident_path
import yaml
from libs.log import getLogger, bold

log = getLogger()


def get_current_incident():
    """
    Gets "current" incident object
    :return: Incident object or None if symlink doesn't exist
    """
    curpath = get_current_incident_path()
    if not os.path.islink(curpath):
        return None

    realpath = os.readlink(get_current_incident_path())
    return Incident.load_by_name(os.path.basename(realpath))


def set_current_incident(incident):
    """
    Sets incident passed as argument as "current"
    :param incident: Incident object to set as "current"
    :return: None
    """
    curpath = get_current_incident_path()
    if os.path.islink(curpath):
        os.unlink(curpath)
    os.symlink(incident.dirpath, curpath)


def find_incident_fullname(partialname):
    """
    Gets list of incidents with specified beginning
    :param partialname: The beginning of incident name
    :return: List of matched incident names
    """
    incidents = os.listdir(get_incidents_path())
    return filter(lambda n: n.startswith(partialname), incidents)


def choose_incident(incident_name, allow_current=True, multiple=False):
    """
    Choosing incident by name provided via arguments
    Should be used by command implementation
    :param incident_name: Incident name (can be partial)
    :param allow_current: Return current if incident_name is empty
    :param multiple: Return list of incidents
    :return: Incident object or list if multiple=True
    """
    if not incident_name or incident_name == "current":
        if not allow_current:
            return None
        current = get_current_incident()
        if current is None:
            log.error("Tried to choose current incident, but no incident found. Use 'switch' to choose one.")
            return None
        return current if not multiple else [current]

    incidents = find_incident_fullname(incident_name)

    if not incidents:
        log.error("No incident found.")
        return None

    if multiple:
        return map(Incident.load_by_name, incidents)
    elif len(incidents) == 1:
        return Incident.load_by_name(incidents[0])
    else:
        log.error("Incident name is ambiguous. Pick one of them:")
        for n in incidents:
            log.info(bold(n))
        return None


class Incident(object):
    def __init__(self, created_on=None,
                 uuid=None, cname=None,
                 closed=False, owner=None,
                 meta=None):
        """
        Constructs incident object
        :param created_on: Creation time as datetime.datetime object (default - now)
        :param uuid: Incident unique id as uuid.uuid4
        :param cname: Keyword which is short description of incident
        :param closed: Is it closed or opened?
        :param owner: Owner name (default - current username)
        :param meta: Dict with custom metadata (tags, IoCs, whatever)
        """
        self.created_on = created_on or datetime.now()
        self.uuid = uuid or uuid4()
        self.cname = cname
        self.closed = closed
        self.owner = owner or get_username()
        self.meta = meta or {}

    @property
    def dirname(self):
        """
        Generates human-friendly directory name for incident files
        :return: str as described above
        """
        return "{}_{}".format(
            self.created_on.strftime("%Y-%m-%d"),
            b32encode(self.uuid.bytes).strip("="))

    @property
    def dirpath(self):
        """
        Returns absolute path to incident files
        :return: str as described above
        """
        return get_incidents_path() + os.sep + self.dirname

    @property
    def metafile(self):
        """
        Returns absolute path of metafile with incident details
        :return: str as described above
        """
        return self.dirpath + os.sep + ".dirt"

    def load(self):
        """
        Loads metadata file with additional informations from storage
        :return: Boolean value, True if success, False otherwise
        """
        if not os.path.isfile(self.metafile):
            return

        with open(self.metafile) as f:
            metadata = yaml.load(stream=f)
        self.cname = metadata.get("cname")
        self.closed = metadata.get("closed", False)
        self.owner = metadata.get("owner", "<unknown>")
        self.meta = metadata.get("meta", {})

    def store(self):
        """
        Stores metadata file with additional informations from storage
        :return: Boolean value, True if success, False otherwise
        """

        # Create incident directory if doesn't exist
        if not os.path.isdir(self.dirpath):
            os.mkdir(self.dirpath)

        metadata = {}
        if self.cname is not None:
            metadata["cname"] = self.cname
        if self.closed:
            metadata["closed"] = True
        if self.owner != "<unknown>":
            metadata["owner"] = self.owner
        if self.meta:
            metadata["meta"] = self.meta
        with open(self.metafile, "w") as f:
            yaml.dump(metadata, stream=f)

    @staticmethod
    def load_by_name(name):
        """
        Creates Incident object for specified stored incident (by name)
        :param name: Full name of incident
        :return Associated Incident object
        """
        timestamp, uuid = name.split("_")
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
        uuid = UUID(bytes=b32decode(uuid+"======"))
        incident = Incident(created_on=timestamp, uuid=uuid)
        if not os.path.isdir(incident.dirpath):
            raise Exception("Incident directory {} not found".format(incident.dirpath))

        try:
            incident.load()
        except Exception as e:
            import traceback
            log.warning("Incident metadata can't be loaded.")
            log.warning(traceback.format_exc())

        return incident

