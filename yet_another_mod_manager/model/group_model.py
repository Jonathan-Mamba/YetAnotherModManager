import abc
import os
import json
import marshmallow
import getpass
import pathlib
import platform
from typing import Iterator, Protocol
from yet_another_mod_manager.config import ModGroup, ConfigFile
from yet_another_mod_manager.util import MetaSingleton
from yet_another_mod_manager.util.enums import ModLoader, MinecraftVersion
from yet_another_mod_manager.util.group import is_valid_group


class SystemStrategy(Protocol):
    @abc.abstractmethod
    def get_config_file_path(self) -> str:
        pass


class GroupModel(metaclass=MetaSingleton):
    def __init__(self, system_strategy: SystemStrategy):
        self._system_strategy = system_strategy
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
            except json.decoder.JSONDecodeError or marshmallow.exceptions.ValidationError:
                pass

    def get_groups(self) -> Iterator[ModGroup]:
        return (i for i in self.config_file.groups)

    def add_group(self, group: ModGroup) -> None:
        if group.name in self.names_set:
            raise ValueError(f"name '{group.name}' is already used")
        elif (is_valid := is_valid_group(group)) and not is_valid[0]:
            raise ValueError(is_valid[1])

        self.config_file.groups.append(group)
        self.names_set.add(group.name)

    def get_group(self, group_name: str) -> ModGroup:
        for group in self.get_groups():
            if group.name == group_name:
                return group
        raise ValueError(f"Group '{group_name}' was not found")

    def remove_group(self, group_name: str):
        if not group_name in self.names_set:
            raise ValueError(None, f"Group '{group_name}' was not found")

        self.config_file.groups = [i for i in self.config_file.groups if i.name != group_name]
        self.names_set.remove(group_name)

    def edit_group(self, group_name: str, new_name: str, new_loader: ModLoader, new_version: MinecraftVersion, force: bool = False):
        if group_name not in self.names_set:
            raise ValueError(f"'{group_name}' was not found")

        is_valid = is_valid_group(ModGroup(name=new_name, mod_loader=new_loader, version=new_version, mods=[]), no_loader=True)
        if not is_valid[0]:
            raise ValueError(is_valid[1])

        if (not force) and (new_name in self.names_set):
            raise ValueError(f"'{new_name}' is already being used")

        if (force) and (new_name in self.names_set):
            self.remove_group(new_name)

        group = self.get_group(group_name)
        group.name = new_name if new_name else group.name
        group.name = new_loader if new_loader else group.mod_loader
        group.version = new_version if new_version else group.version

    def get_config_file_path(self) -> str:
        return self._system_strategy.get_config_file_path()

    def install_group(self, group: str, folder: pathlib.Path):
        pass

    def save(self) -> None:
        with open(self.get_config_file_path(), "w") as f:
            f.write(self.config_file.to_json())


class PosixStategy(SystemStrategy):
    def get_config_file_path(self) -> str:
        return pathlib.Path(f"/home/{getpass.getuser()}/.config/yet-another-mod-manager/config.json")
    
class WindowsStrategy(SystemStrategy):
    def get_config_file_path(self) -> str:
        return pathlib.Path(os.getenv("APPDATA")) / ".yet-another-mod-manager" / "config.json"


def get_group_model() -> GroupModel:
    """:returns the correct model corresponding to the platform"""
    try: 
        return GroupModel()
    except TypeError: 
        return GroupModel(PosixStategy() if platform.system() != "Windows" else WindowsStrategy())