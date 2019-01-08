import os

DIRT_DIR = os.path.expanduser("~/.dirt")


def get_incidents_path():
    path = os.path.join(DIRT_DIR, 'data')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_current_incident_path():
    return os.path.join(get_incidents_path(), 'current')


def get_history_path():
    return os.path.join(get_incidents_path(), 'history')


def get_plugins_path():
    path = os.path.join(DIRT_DIR, 'plugins')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_tags_path():
    path = os.path.join(DIRT_DIR, 'tags')
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def get_tag_path(tag, create=True):
    path = os.path.join(get_tags_path(), tag)
    if not os.path.exists(path):
        if create:
            os.makedirs(path)
        else:
            return None
    return path
