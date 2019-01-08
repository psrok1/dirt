import os, pwd
import glob
import yaml

import click


def is_dir_traversal(file_name, rel_directory):
    requested_path = os.path.abspath(file_name)
    common_prefix = os.path.commonprefix([requested_path, rel_directory])
    return common_prefix != rel_directory


def get_username():
    return pwd.getpwuid(os.getuid())[0]


def get_tty_width():
    _, columns = os.popen('stty size', 'r').read().split()
    return int(columns)


def pprint_obj(obj):
    class SetAsListDumper(yaml.Dumper):
        def __init__(self, *args, **kwargs):
            super(SetAsListDumper, self).__init__(*args, **kwargs)
            print("Dumper enabled")

        def represent_mapping(self, *args, **kwargs):
            tag, data = args
            mapping = super(SetAsListDumper, self).represent_mapping(*args, **kwargs)
            if tag.endswith("set"):
                return self.represent_list(list(data))
            else:
                return mapping

    return yaml.dump(obj, default_flow_style=False, Dumper=SetAsListDumper)
