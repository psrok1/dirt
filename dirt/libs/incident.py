import os, re
import yaml
from base64 import b32encode, b32decode
from datetime import datetime
from uuid import uuid4, UUID

from dirt.libs.path import get_incidents_path, get_current_incident_path, get_tag_path, get_tags_path
from dirt.libs.log import *
from dirt.libs.utils import get_username, get_tty_width, is_dir_traversal
from dirt.libs.history import push_history, get_previous_incident

KEYWORDS = ["overview", "all", "history", "current", "previous"]


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
    current = get_current_incident()
    if current:
        push_history(current)
    curpath = get_current_incident_path()
    if os.path.islink(curpath):
        os.unlink(curpath)
    os.symlink(incident.dirpath, curpath)


def find_incidents(partialname="", path=None):
    """
    Gets sorted list of incidents with specified beginning
    :param partialname: The beginning of incident name
    :return: List of matched incident names
    """
    incidents = os.listdir(path or get_incidents_path())
    # Filter out all dirs with invalid name
    incidents = [n for n in incidents if re.match(r"^\d{4}-\d{2}-\d{2}_[A-Z2-7]{26}$", n)]
    # Filter all dirs with specified beginning
    incidents = filter(lambda n: n.startswith(partialname), incidents)
    # Show current incident first
    current = get_current_incident()
    return sorted(incidents, key=lambda n: "A" if current and current.identifier == n else n, reverse=True)


def find_tags(partialname="", path=None):
    tags = os.listdir(path or get_tags_path())
    return sorted([tag for tag in tags if tag.startswith(partialname.lower())])


def load_all_incidents():
    return map(Incident.load_by_name, find_incidents())


def find_incidents_by_tag(tag_name):
    tag = get_tag_path(tag_name, create=False)
    if tag is None:
        return []
    incidents = find_incidents(path=tag)
    return incidents


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
            error("Tried to load current incident, but no incident found. Use 'new' or 'switch' to get one.")
            return None
        return current if not multiple else [current]

    if incident_name == "previous":
        current = get_previous_incident()
        if current is None:
            error("Tried to load previous incident, but history is empty.")
            return None
        return current if not multiple else [current]

    incidents = find_incidents(partialname=incident_name)

    if not incidents:
        return None

    if multiple:
        return list(map(Incident.load_by_name, incidents))
    elif len(incidents) == 1:
        return Incident.load_by_name(incidents[0])
    else:
        warning("Incident name is ambiguous. Pick one of them:")
        for n in incidents:
            echo("{incident_id}", incident_id=n, ignore_short=True)
        return None


def is_incident_partial_name(partial_name):
    if partial_name in ["current", "previous"]:
        return True
    if len(partial_name) >=6 and re.match(r"^\d{4}-\d{2}", partial_name[:6]):
        return True
    return False


def expand_incident_arg(arg):
    if ":" not in arg:
        return arg

    name, path = arg.split(":", 1)
    if not is_incident_partial_name(name):
        return arg

    current = choose_incident(name)
    if current is None:
        raise RuntimeError("Incident {} not found.".format(name))

    path = os.path.join(current.dirpath, path)
    if is_dir_traversal(path, rel_directory=current.dirpath):
        raise RuntimeError("Path is out of {} root directory".format(current.identifier))

    return path


class IncidentCompleter(object):
    def __init__(self, additional_choices=None):
        self.choices = additional_choices or []

    def __call__(self, **kw):
        return find_incidents() + self.choices


class Incident(object):
    def __init__(self, created_on=None,
                 uuid=None, cname=None,
                 closed=False, owner=None,
                 meta=None, tags=None):
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
        self.tags = tags or set()

    def __eq__(self, other):
        return self.uuid == other.uuid

    @property
    def identifier(self):
        """
        Generates human-friendly directory name for incident files
        :return: str as described above
        """
        return "{}_{}".format(
            self.created_on.strftime("%Y-%m-%d"),
            b32encode(self.uuid.bytes).decode("utf-8").strip("="))

    @property
    def dirpath(self):
        """
        Returns absolute path to incident files
        :return: str as described above
        """
        return get_incidents_path() + os.sep + self.identifier

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
            metadata = yaml.safe_load(stream=f)
        self.cname = metadata.get("cname")
        self.closed = metadata.get("closed", False)
        self.owner = metadata.get("owner", "<unknown>")
        self.meta = metadata.get("meta", {})
        self.tags = metadata.get("tags", set())

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
        if self.tags:
            metadata["tags"] = self.tags
        with open(self.metafile, "w") as f:
            yaml.dump(metadata, stream=f)

    def add_meta(self, key, value, type=None):
        if type is not None:
            if key not in self.meta:
                # If key doesn't exist - create collection
                self.meta[key] = type()
            elif not isinstance(self.meta[key], list) and not isinstance(self.meta[key], set):
                # If key exists yet but it's scalar - convert to collection
                self.meta[key] = type([self.meta[key]])
            else:
                # If key exists and is collection yet - convert between types
                self.meta[key] = type(self.meta[key])

        if key in self.meta:
            if isinstance(self.meta[key], list):
                self.meta[key].append(value)
                return
            elif isinstance(self.meta[key], set):
                self.meta[key].add(value)
                return
        self.meta[key] = value

    def remove_meta(self, key, value=None):
        if key not in self.meta:
            return
        if value is not None and type(self.meta[key]) in [set, list]:
            self.meta[key].remove(value)
            if not self.meta[key]:
                del self.meta[key]
        else:
            del self.meta[key]

    def normalize_tag(self, tag):
        tag = tag.lower()
        p = re.compile(r"^[a-z][a-z0-9_\-]{1,31}$")
        if not p.match(tag) or tag in KEYWORDS:
            return None
        return tag

    def add_tag(self, tag):
        tag = self.normalize_tag(tag)
        if tag is None:
            return None
        if tag not in self.tags:
            self.tags.add(tag)
            os.symlink(self.dirpath, os.path.join(get_tag_path(tag), self.identifier))
        return tag

    def remove_tag(self, tag):
        tag = self.normalize_tag(tag)
        if tag is None:
            return
        if tag not in self.tags:
            return
        link_path = os.path.join(get_tag_path(tag), self.identifier)
        self.tags.remove(tag)
        if os.path.islink(link_path):
            os.unlink(link_path)
        return tag

    def add_relation(self, other):
        self.add_meta("relation", other.identifier, type=set)
        os.symlink(other.dirpath, os.path.join(self.dirpath, other.identifier))

    def remove_relation(self, other):
        self.remove_meta("relation", other.identifier)
        link_path = os.path.join(self.dirpath, other.identifier)
        if os.path.islink(link_path):
            os.unlink(link_path)

    @staticmethod
    def load_by_name(name):
        """
        Creates Incident object for specified stored incident (by name)
        :param name: Full name of incident
        :return Associated Incident object
        """
        if "_" not in name:
            return None
        timestamp, uuid = name.split("_", 1)
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d")
        uuid = UUID(bytes=b32decode(uuid+"======"))
        incident = Incident(created_on=timestamp, uuid=uuid)
        if not os.path.isdir(incident.dirpath):
            raise Exception("Incident directory {} not found".format(incident.dirpath))

        try:
            incident.load()
        except Exception as e:
            import traceback
            warning("Incident {incident} metadata can't be loaded", incident=name)
            warning(traceback.format_exc())

        return incident

