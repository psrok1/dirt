import os
from dirt.libs.path import get_history_path

HISTORY_LENGTH = 20


def read_history():
    from dirt.libs.incident import Incident
    if not os.path.isfile(get_history_path()):
        return []
    with open(get_history_path()) as f:
        return list(filter(None, [Incident.load_by_name(incident_id.strip()) for incident_id in f.readlines()]))


def write_history(incidents):
    with open(get_history_path(), "w") as f:
        f.write('\n'.join([inc.identifier for inc in incidents][-HISTORY_LENGTH:]))


def get_previous_incident():
    history = read_history()
    return history[-1] if history else None


def push_history(incident):
    write_history(read_history() + [incident])

