import typer
from rich.table import Table
from rich.console import Console
from rich import box
from mc_mod_config.model import get_model
from mc_mod_config.util import ModGroup


def add(name: str, loader: str, version: str):
    get_model().add_group(ModGroup(name=name, mod_loader=loader, version=version, mods=[]))
    get_model().save()


def remove(name: str):
    get_model().remove_group(name)
    get_model().save()


def list_groups() -> None:
    if not get_model().names_set:
        return

    table = Table("NAME", "LOADER", "VERSION", "MOD_COUNT", box=box.HORIZONTALS)

    for group in get_model().get_groups():
        table.add_row(group['name'], group['mod_loader'], group['version'], str(len(group['mods'])))

    Console().print(table)

def edit(group: str, name: str = "", loader: str = "", version: str = "", force: bool = False) -> None:
    get_model().edit_group(group, name, loader, version, force)
    get_model().save()