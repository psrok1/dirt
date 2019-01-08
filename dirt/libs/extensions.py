import click
import importlib
import pkgutil

from dirt.libs.path import get_plugins_path

import dirt_plugins

dirt_plugins.__spec__.submodule_search_locations.append(get_plugins_path())


class DirtPluginInstance(object):
    def __init__(self, name):
        self.name = name
        self.module = importlib.import_module(name)
        self.hooks = self.get_submodule("hooks")
        if self.hooks:
            for loader, module_name, is_pkg in pkgutil.walk_packages(self.hooks.__path__):
                loader.find_module(module_name).load_module(module_name)

    def has_submodule(self, submodule):
        submodule = self.name + "." + submodule
        return importlib.util.find_spec(submodule)

    def get_submodule(self, submodule):
        submodule = self.name+"."+submodule
        return importlib.util.find_spec(submodule) and importlib.import_module(submodule)


PLUGINS = [
    DirtPluginInstance(name)
    for finder, name, ispkg
    in pkgutil.iter_modules(dirt_plugins.__path__, dirt_plugins.__name__ + ".")
]


def register_subcommands(group, modules, attribute):
    # Import all submodules
    for module in modules:
        for loader, module_name, is_pkg in pkgutil.walk_packages(module.__path__):
            command = getattr(loader.find_module(module_name).load_module(module_name), attribute, None)
            if command is not None:
                group.add_command(command)


def get_submodule_plugins(submodule):
    return [plugin.get_submodule(submodule) for plugin in PLUGINS if plugin.has_submodule(submodule)]


def extendable_group(handler_factory, completer=None):
    class ExtendableGroup(click.Group):
        def __init__(self, *args, **kwargs):
            super(ExtendableGroup, self).__init__(*args, **kwargs)
            self.help_context = False

        def format_commands(self, ctx, formatter):
            self.help_context = True
            try:
                return super(ExtendableGroup, self).format_commands(ctx, formatter)
            finally:
                self.help_context = False

        def list_commands(self, ctx):
            return super(ExtendableGroup, self).list_commands(ctx) + \
                   ([] if self.help_context or not completer else completer(ctx, [], ""))

        def get_command(self, ctx, command):
            predefined = super(ExtendableGroup, self).get_command(ctx, command)
            if predefined is not None:
                return predefined
            else:
                return handler_factory(ctx, command)
    return ExtendableGroup


def passthrough_group(secondary_group):
    class PassthroughGroup(click.Group):
        def list_commands(self, ctx):
            return super(PassthroughGroup, self).list_commands(ctx) + secondary_group.list_commands(ctx)

        def get_command(self, ctx, command):
            predefined = super(PassthroughGroup, self).get_command(ctx, command)
            if predefined is not None:
                return predefined
            else:
                return secondary_group.get_command(ctx, command)
    return PassthroughGroup
