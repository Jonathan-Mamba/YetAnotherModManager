import typer
from typing_extensions import Literal
from src.util import ModGroup
from src.model import get_model
from src.view.util import App, Stream

"""
Remaining:
    - edit
    - search
    - install
"""

app = App()

def run_cli():
    App()()
    print("c'est bon c fini")
    get_model().save()


@app.command(name="list")
def list_groups() -> None:
    """
    Lists all groups in a similar manner to git log
    """
    stream = Stream()
    for group in get_model().get_groups():
        finished = not stream.print_line(f"GROUP {group['name']} ({group["mod_loader"]} {group["version"]}):")
        if finished:
            return
        for mod in group['mods']:
            finished = not stream.print_line(f"- {mod}")
            if finished:
                return



@app.command(help="Adds a new group without any mods")
def add(name: str, loader: str, version: str):
    get_model().add_group(ModGroup(name=name, mod_loader=loader, version=version, mods=[]))
    typer.echo(f"Group '{name}' was created successfully.")



@app.command(help="Removes a local group (permanent)")
def remove(name: str):
    get_model().remove_group(name)
    typer.echo(f"Group '{name}' was removed successfully.")



