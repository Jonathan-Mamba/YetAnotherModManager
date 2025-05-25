import typer
from typing import Annotated
from mc_mod_config.view.cli import bulk
from mc_mod_config.util import MetaSingleton

"""
Remaining:
    - edit
    - search
    - install
"""

class App(typer.Typer, metaclass=MetaSingleton):
    """
    Singleton class that contains a reference to the app
    """
    def __init__(self):
        super().__init__(no_args_is_help=True)


app = App()

@app.command(name="list", help="Lists all local groups")
def list_groups() -> None:
    bulk.list_groups()



@app.command(help="Adds a new group without any mods", no_args_is_help=True)
def add(
        name: Annotated[str, typer.Argument("Name of the created group")],
        loader: Annotated[str, typer.Argument("Mod loader of the created group")],
        version: Annotated[str, typer.Argument("Version of the created group")]
) -> None:
    try:
        bulk.add(name, loader, version)
    except ValueError as e:
        typer.echo(f"ERROR: {e}")
    else:
        typer.echo(f"Group '{name}' was created successfully")



@app.command(help="Removes a local group (permanent)", no_args_is_help=True)
def remove(name: Annotated[str, typer.Argument(help="Name of the group")]):
    try:
        bulk.remove(name)
    except ValueError as e:
        typer.echo(f"ERROR: {e}")
    else:
        typer.echo(f"Group '{name}' was removed successfully.")


@app.command(help="Edits properties of a group", no_args_is_help=True)
def edit(
        group: Annotated[str, typer.Argument(help="Name of the edited group")],
        name: Annotated[str, typer.Option(help="New name of the group")] = "",
        loader: Annotated[str, typer.Option(help="New mod loader of the group")] = "",
        version: Annotated[str, typer.Option(help="New version of the group")] = ""
) -> None:
    bulk.edit(group, name, loader, version)
