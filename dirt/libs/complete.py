import glob
import os

from dirt.libs import incident


def incident_expand_arg_list(partial):
    if ":" in partial:
        name, relpath = partial.split(":", 1)
        try:
            current = incident.choose_incident(name)
            return path_list(relpath, relpath=current.dirpath)
        except RuntimeError:
            return []
    else:
        return [inc+":" for inc in incident_list(partial) if inc.startswith(partial)] + path_list(partial)


def tags_list(partial):
    return incident.find_tags(partial)


def incident_list(partial):
    return incident.find_incidents(partial) + ["current", "previous"]


def path_list(partial, relpath="."):
    origin = os.path.abspath(relpath)
    return [os.path.relpath(variant, origin) + ("/" if os.path.isdir(variant) else "")
            for variant in glob.glob(os.path.join(origin, partial+"*"))]


def completer(partial, *varlists):
    return sorted(list(set([var for vlist in varlists for var in vlist(partial) if var.startswith(partial)])))


def get_completer(*varlists):
    def get_variants(ctx, args, incomplete):
        return completer(incomplete, *varlists)
    return get_variants
