import os
import getpass
import pathlib
from typing import Self
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from yet_another_mod_manager.util.enums import MinecraftVersion, ModLoader, Platform, Channel


posix_config_path = pathlib.Path(f"/home/{getpass.getuser()}/.var/app/yet-another-mod-manager/groups.json")
windows_config_path = pathlib.Path(os.getenv("APPDATA", "/")) / ".yet-another-mod-manager" / "groups.json"


@dataclass_json
@dataclass
class Mod:
    slug: str
    version: str = "latest"
    channel: Channel = Channel.ANY
    platform: Platform = Platform.MODRINTH


@dataclass_json
@dataclass
class ModGroup:
    name: str
    mod_loader: ModLoader
    version: MinecraftVersion
    mods: list[Mod]


@dataclass_json
@dataclass
class ConfigFile:
    groups: list[ModGroup]

    @classmethod
    def empty(cls) -> Self:
        return cls(groups=[])
