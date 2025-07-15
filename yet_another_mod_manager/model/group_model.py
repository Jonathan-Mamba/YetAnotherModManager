import abc
import os
import json
import marshmallow
import getpass
import pathlib
import platform
from typing import Iterator, Protocol
from yet_another_mod_manager.config import ModGroup, ConfigFile, posix_config_path, windows_config_path
from yet_another_mod_manager.util import MetaSingleton, CommandError
from yet_another_mod_manager.util.group import is_valid_group



class GroupModel(metaclass=MetaSingleton):
    def __init__(self):
        self._config_file: ConfigFile = ConfigFile.empty()
        self.load()

        self.names_set: set[str] = {i.name for i in self.config_file.groups}

    @property
    def config_file(self) -> ConfigFile:
        return self._config_file


    def load(self):
        # making sure that the config file does exists
        if not os.path.exists(self.get_config_file_path()):
            
            if not os.path.exists(os.path.dirname(self.get_config_file_path())):
                os.makedirs(os.path.dirname(self.get_config_file_path()))
            
            with open(self.get_config_file_path(), "a") as f:
                f.write(json.dumps(ConfigFile.empty().to_dict()))

        with open(self.get_config_file_path(), 'r') as f:
            try:
                self._config_file = ConfigFile.schema().loads(f.read())
            except marshmallow.exceptions.ValidationError:
                raise CommandError('Could not load the group data, Invalid file format')
            except json.decoder.JSONDecodeError:
                raise CommandError('Could not load the group data, Invalid file format')


    def get_groups(self) -> Iterator[ModGroup]:
        return (i for i in self.config_file.groups)


    def add_group(self, group: ModGroup) -> None:
        if group.name in self.names_set:
            raise CommandError(f"name '{group.name}' is already used")
        elif (is_valid := is_valid_group(group)) and not is_valid[0]:
            raise CommandError(is_valid[1])

        self.config_file.groups.append(group)
        self.names_set.add(group.name)


    def get_group(self, group_name: str) -> ModGroup:
        for group in self.get_groups():
            if group.name == group_name:
                return group
        raise CommandError(f"Group '{group_name}' was not found")


    def remove_group(self, group_name: str):
        if not group_name in self.names_set:
            raise CommandError(None, f"Group '{group_name}' was not found")

        self.config_file.groups = [i for i in self.config_file.groups if i.name != group_name]
        self.names_set.remove(group_name)


    def edit_group(self, new_group: ModGroup, old_name: str, force: bool = False):
        is_valid = is_valid_group(new_group, no_loader=True)
        if not is_valid[0]:
            raise CommandError(is_valid[1])

        if (not force) and (new_group.name in self.names_set - {old_name}):
            raise CommandError(f"'{new_group.name}' is already being used")

        old_group = self.get_group(old_name)
        old_group.name = new_group.name
        old_group.mod_loader = new_group.mod_loader
        old_group.version = new_group.version
        old_group.mods = new_group.mods


    def get_config_file_path(self) -> pathlib.Path:
        return posix_config_path if platform.system() != "Windows" else windows_config_path


    def install_group(self, group: str, folder: pathlib.Path):
        pass


    def save(self) -> None:
        with open(self.get_config_file_path(), "w") as f:
            f.write(self.config_file.to_json())


def get_group_model() -> GroupModel:
    """:returns the correct model corresponding to the platform"""
    return GroupModel()