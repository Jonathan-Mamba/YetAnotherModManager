import typer
from typing import Annotated
from mc_mod_config.view.cli import bulk
from mc_mod_config.util import MetaSingleton

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

@app.command(name="list", help="Lists all local groups")
def list_groups() -> None:
    bulk.list_groups()



@app.command(help="Adds a new group without any mods", no_args_is_help=True)
def add(
        name: Annotated[str, typer.Argument(help="Name of the created group")],
        loader: Annotated[str, typer.Argument(help="Mod loader of the created group")],
        version: Annotated[str, typer.Argument(help="Version of the created group")]
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
        version: Annotated[str, typer.Option(help="New version of the group")] = "",
        force: Annotated[bool, typer.Option(help="Override existing group if the new name is already used")] = False
) -> None:
    try:
        bulk.edit(group, name, loader, version, force)
    except ValueError as e:
        typer.echo(f"ERROR: {e}")
    else:
        typer.echo(f"Group '{group}' was modified successfully.")



@app.command(help="Search a mod using the modrinth api", no_args_is_help=True)
def search(
        query: Annotated[str, typer.Argument(help="Name of the searched mod")],
        index: Annotated[str, typer.Option(help="Sorting method of the results ('relevance', 'downloads', 'follows', 'newest', 'updated')")] = 'relevance',
        offset: Annotated[int, typer.Option(help="The offset into the search. Skips this number of results")] = 0,
        limit: Annotated[int, typer.Option(help="The number of results returned by the search. must be <= 100")] = 10
):
    try:
        bulk.search(query, index, offset, limit)
    except ValueError as e:
        typer.echo(e)



@app.command(help="Installs a group into a folder. Does not check for other files")
def install(
        group: Annotated[str, typer.Argument("The name of the installed group")],
        folder: Annotated[str, typer.Argument("The folder where the group will be installed")]
)