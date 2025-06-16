import abc
import os
import json
import getpass
import pathlib

from yet_another_mod_manager import util
from typing import Iterator, Protocol


class SystemStrategy(Protocol):
    @abc.abstractmethod
    def get_config_file_path(self) -> str:
        pass


class GroupModel(metaclass=util.MetaSingleton):
    def __init__(self, system_strategy: SystemStrategy):
        self._system_strategy = system_strategy

        if not os.path.exists(self.get_config_file_path()):
            if not os.path.exists(os.path.dirname(self.get_config_file_path())):
                os.makedirs(os.path.dirname(self.get_config_file_path()))
            with open(self.get_config_file_path(), "a") as f:
                f.write(json.dumps(util.ConfigFile(groups=[])))

        with open(self.get_config_file_path(), "r") as f:
            try:
                self._config_dict: util.ConfigFile = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                with open(self.get_config_file_path(), "a") as f:
                    f.write(json.dumps(util.ConfigFile(groups=[])))
                self._config_dict: util.ConfigFile = {"groups": []}

        self.names_set: set[str] = {i.get("name") for i in self._config_dict["groups"]}

    def get_groups(self) -> Iterator[util.ModGroup]:
        return (i for i in self._config_dict["groups"])

    def add_group(self, group: util.ModGroup) -> None:
        if group["name"] in self.names_set:
            raise ValueError(f"name '{group['name']}' is already used")
        elif (is_valid := util.check_group_validity(group)) and not is_valid[0]:
            raise ValueError(is_valid[1])

        self._config_dict["groups"].append(group)
        self.names_set.add(group['name'])

    def get_group(self, group_name: str):
        for group in self.get_groups():
            if group['name'] == group_name:
                return group
        raise ValueError(f"Group '{group_name}' was not found")

    def remove_group(self, group_name: str):
        if not group_name in self.names_set:
            raise ValueError(None, f"Group '{group_name}' was not found")

        self._config_dict['groups'] = [i for i in self._config_dict['groups'] if i['name'] != group_name]
        self.names_set.remove(group_name)

    def edit_group(self, group_name: str, new_name: str, new_loader: str, new_version: str, force: bool = False):
        if group_name not in self.names_set:
            raise ValueError(f"'{group_name}' was not found")

        is_valid = util.check_group_validity(util.ModGroup(name=new_name, mod_loader=new_loader, version=new_version, mods=[]), no_loader=True)
        if not is_valid[0]:
            raise ValueError(is_valid[1])

        if (not force) and (new_name in self.names_set):
            raise ValueError(f"'{new_name}' is already being used")

        if (force) and (new_name in self.names_set):
            self.remove_group(new_name)

        group = self.get_group(group_name)
        group['name'] = new_name if new_name else group['name']
        group['mod_loader'] = new_loader if new_loader else group['mod_loader']
        group['version'] = new_version if new_version else group['version']

    def get_config_file_path(self) -> str:
        return self._system_strategy.get_config_file_path()

    def install_group(self, group: str, folder: pathlib.Path):
        pass

    def save(self) -> None:
        with open(self.get_config_file_path(), "w") as f:
            f.write(json.dumps(self._config_dict, indent=2))


class LinuxStategy(SystemStrategy):
    def get_config_file_path(self) -> str:
        return f"/home/{getpass.getuser()}/.config/minecraft-mod-config.json"


def get_group_model() -> GroupModel:
    """:returns the correct model corresponding to the platform"""
    try: return GroupModel()
    except TypeError: return GroupModel(LinuxStategy())