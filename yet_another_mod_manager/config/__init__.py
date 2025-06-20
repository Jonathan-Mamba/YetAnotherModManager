from dataclasses_json import dataclass_json
from dataclasses import dataclass
from yet_another_mod_manager.util.enums import MinecraftVersion, ModLoader
from typing import Self


@dataclass_json
@dataclass
class ModGroup:
    name: str
    mod_loader: ModLoader
    version: MinecraftVersion
    mods: list[str]


@dataclass_json
@dataclass
class ConfigFile:
    groups: list[ModGroup]

    @classmethod
    def empty(cls) -> Self:
        return cls(groups=[])
    
    
