import os
import pwd
import subprocess


def is_dir_traversal(file_name):
    current_directory = os.path.abspath(os.curdir)
    requested_path = os.path.relpath(file_name, start=current_directory)
    requested_path = os.path.abspath(requested_path)
    common_prefix = os.path.commonprefix([requested_path, current_directory])
    return common_prefix != current_directory


def get_username():
    return pwd.getpwuid(os.getuid())[0]


def ask(msg):
    answer = raw_input("{} y/[n]: ".format(msg))
    return answer.lower().startswith("y")


def ask_str(msg):
    answer = raw_input("{}: ".format(msg))
    return answer


def locate_file(fname):
    path = os.environ.get("PATH", "").split(os.pathsep)
    for p in path:
        fn = p + os.sep + fname
        if os.path.isfile(fn):
            return fn
    return None


def open_editor(fname):
    editor = os.environ.get("EDITOR", locate_file("nano"))
    if editor is None:
        editor = locate_file("vi")
    if editor is None:
        raise Exception("Suitable editor not found. Set editor in $EDITOR env.")
    subprocess.call([editor, fname])
    return os.path.isfile(fname)
