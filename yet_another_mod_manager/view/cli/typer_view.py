import typer
import pathlib
from typing import Annotated
from requests.exceptions import ConnectionError
from yet_another_mod_manager.view.cli import bulk
from yet_another_mod_manager.util import MetaSingleton, enums, CommandError
"""
Remaining:
    - install
"""

class App(typer.Typer, metaclass=MetaSingleton):
    """
    Singleton class that contains a reference to the app
    """
    def __init__(self):
        super().__init__(no_args_is_help=True)


app = App()

@app.command(name="list", help="Lists all local groups.")
def list_groups() -> None:
    try:
        bulk.list_groups()
    except CommandError as e:
        typer.echo(f"ERROR: {e}")


@app.command(name="print", help="Prints the data of a group.", no_args_is_help=True)
def print_group(group: Annotated[str, typer.Argument(help="Name of the group.")]):
    try:
        bulk.print_group(group)
    except CommandError as e:
        typer.echo(f"ERROR: {e}")



@app.command(help="Adds a new group without any mods.", no_args_is_help=True)
def add(
        name: Annotated[str, typer.Argument(help="Name of the created group")],
        loader: Annotated[enums.ModLoader, typer.Argument(help="Mod loader of the created group")],
        version: Annotated[enums.MinecraftVersion, typer.Argument(help="Version of the created group")]
) -> None:
    try:
        bulk.add(name, loader, version)
    except ValueError as e:
        typer.echo(f"ERROR: {e}.")
    else:
        typer.echo(f"Group '{name}' was created successfully.")



@app.command(help="Removes a local group (permanent).", no_args_is_help=True)
def remove(name: Annotated[str, typer.Argument(help="Name of the group.")]):
    try:
        bulk.remove(name)
    except ValueError as e:
        typer.echo(f"ERROR: {e}")
    else:
        typer.echo(f"Group '{name}' was removed successfully.")



@app.command(help="Edits properties of a group.", no_args_is_help=True)
def edit(
        group: Annotated[str, typer.Argument(help="Name of the edited group.")],
        force: Annotated[bool, typer.Option(help="Override existing group if the new name is already used.")] = False
) -> None:
    try:
        bulk.edit(group, force)
    except CommandError as e:
        typer.echo(f"ERROR: {e}")
    else:
        typer.echo(f"Group '{group}' was modified successfully.")



@app.command(help="Searches a mod using the modrinth api.", no_args_is_help=True)
def search(
        query: Annotated[str, typer.Argument(help="Name of the searched mod.")],
        index: Annotated[enums.ModrinthSearchIndex, typer.Option(help="Sorting method of the results ('relevance', 'downloads', 'follows', 'newest', 'updated').")] = 'relevance',
        offset: Annotated[int, typer.Option(help="The offset into the search. Skips this number of results.")] = 0,
        limit: Annotated[int, typer.Option(help="The number of results returned by the search. must be <= 100.")] = 10
):
    try:
        bulk.search(query, index, offset, limit)
    except ValueError or ConnectionError as e:
        typer.echo(e)



@app.command(help="Installs a group into a folder. Does not check for other files.", no_args_is_help=True)
def install(
        group: Annotated[str, typer.Argument(help="The name of the installed group.")],
        folder: Annotated[pathlib.Path, typer.Argument(help="The folder where the group will be installed.", resolve_path=True, exists=True, dir_okay=True, writable=True)]
):
    typer.echo("Not implemented yet.")



@app.command(help="Launch the graphical interface.")
def gui() -> None:
    typer.echo("Not implemented yet.")


@app.command(help="Open the config file.")
def config():
    bulk.config()
