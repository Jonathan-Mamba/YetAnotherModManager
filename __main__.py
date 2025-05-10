import abc
import json
import util
import getpass

class Model(abc.ABC):
    @abc.abstractmethod
    def get_config_json(self) -> dict:
        pass

    @abc.abstractmethod
    def add_group(self, group: util.ModGroup) -> None:
        pass

class LinuxModel(Model):
    def get_config_json(self):
        with open(f"/home/{getpass.getuser}/.config/minecraft-mod-config.json", "r") as f:
            return json.loads(f.read())

def main():
    pass

if __name__ == "__main__":
    main()