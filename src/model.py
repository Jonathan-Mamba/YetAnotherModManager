import argparse
import os
import abc
import util
import json
import getpass
from argparse import ArgumentError
from typing import Iterator

class Model(abc.ABC):
    def __init__(self):
        if not os.path.exists(self.config_file_path()):
            if not os.path.exists(os.path.dirname(self.config_file_path())):
                os.makedirs(os.path.dirname(self.config_file_path()))
            with open(self.config_file_path(), "a") as f:
                f.write("""{"groups":[]}""")

        with open(self.config_file_path(), "r") as f:
            try:
                self._config_dict: util.ConfigFile = json.loads(f.read())
            except json.decoder.JSONDecodeError:
                with open(self.config_file_path(), "a") as f:
                    f.write("""{"groups":[]}""")
                self._config_dict: util.ConfigFile = {"groups":[]}

        self.names_set: set[str] = {i.get("name") for i in self._config_dict["groups"]}

    def get_groups(self) -> Iterator[util.ModGroup]:
        return (i for i in self._config_dict["groups"])

    @abc.abstractmethod
    def config_file_path(self) -> str:
        pass

    def add_group(self, group: util.ModGroup) -> None:
        if group["name"] in self.names_set:
            raise ArgumentError(None, f"name {group['name']} is already used")
        elif group["mod_loader"] not in util.modloaders:
            raise ArgumentError(None, f"The only valid modloaders are {util.modloaders}, not {group['mod_loader']}")

        self._config_dict["groups"].append(group)
        self.names_set.add(group['name'])

    def remove_group(self, group_name: str):
        if not group_name in self.names_set:
            raise argparse.ArgumentError(None, f"{group_name} was not found")

        self._config_dict['groups'] = [i for i in self._config_dict['groups'] if i['name'] != group_name]
        self.names_set.remove(group_name)

    @abc.abstractmethod
    def save(self) -> None:
        pass

    @abc.abstractmethod
    def clear_screen(self):
        pass


class LinuxModel(Model):
    def config_file_path(self) -> str:
        return f"/home/{getpass.getuser()}/.config/minecraft-mod-config.json"

    def save(self) -> None:
        with open(self.config_file_path(), "w") as f:
            f.write(json.dumps(self._config_dict))

    def clear_screen(self):
        os.system("clear")