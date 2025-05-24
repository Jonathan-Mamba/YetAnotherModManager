from src.model import get_model
from src.util import ModGroup
from src.view.util import Stream
from typing import Literal
import typer



def add(name: str, loader: str, version: str):
    get_model().add_group(ModGroup(name=name, mod_loader=loader, version=version, mods=[]))
    get_model().save()


def remove(name: str):
    get_model().remove_group(name)
    get_model().save()
    typer.echo(f"Group '{name}' was removed successfully.")


def list_groups() -> None:
    stream = Stream()
    for group in get_model().get_groups():
        finished = not stream.print_line(f"GROUP {group['name']} ({group["mod_loader"]} {group["version"]}):")
        if finished:
            return
        for mod in group['mods']:
            finished = not stream.print_line(f"- {mod}")
            if finished:
                return

def edit(group: str, name: str, loader: str, version: str) -> None:
    pass