import typer
from mc_mod_config.view.util import App
from mc_mod_config.view.cli import bulk

"""
Remaining:
    - edit
    - search
    - install
"""

app = App()
app2 = App()


@app.command(name="list", help="Lists all local groups")
def list_groups() -> None:
    bulk.list_groups()



@app.command(help="Adds a new group without any mods", no_args_is_help=True)
def add(name: str, loader: str, version: str):
    try:
        bulk.add(name, loader, version)
    except ValueError as e:
        typer.echo(f"ERROR: {e}")
    else:
        typer.echo(f"Group '{name}' was created successfully")



@app.command(help="Removes a local group (permanent)", no_args_is_help=True)
def remove(name: str):
    try:
        bulk.remove(name)
    except ValueError as e:
        typer.echo(f"ERROR: {e}")
    else:
        typer.echo(f"Group '{name}' was removed successfully.")


@app.command(help="Edits properties of a group", no_args_is_help=True)
def edit(group: str, name: str = "", loader: str = "", version: str = "") -> None:
    """
    Edits properties of a group
    :param group: name of the edited group
    :param name: new name of the group
    :param loader: new loader of the group
    :param version: new version of the group
    """
    bulk.edit(group, name, loader, version)
