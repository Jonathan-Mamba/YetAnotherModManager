from typing import TypedDict, Literal


class ModGroup(TypedDict):
    mod_loader: Literal["fabric", "forge", "neoforge", "quilt"]
    version: str
    mods: list[str]
