import typer
import requests
from rich.table import Table
from rich.console import Console
from rich import box
from mc_mod_config.model import get_group_model, get_api_model
from mc_mod_config.util import ModGroup


def add(name: str, loader: str, version: str):
    get_group_model().add_group(ModGroup(name=name, mod_loader=loader, version=version, mods=[]))
    get_group_model().save()


def remove(name: str):
    get_group_model().remove_group(name)
    get_group_model().save()


def list_groups() -> None:
    if not get_group_model().names_set:
        return

    table = Table("NAME", "LOADER", "VERSION", "MOD_COUNT", box=box.HORIZONTALS)
    for group in get_group_model().get_groups():
        table.add_row(group['name'], group['mod_loader'], group['version'], str(len(group['mods'])))

    Console().print(table)



def edit(group: str, name: str = "", loader: str = "", version: str = "", force: bool = False) -> None:
    get_group_model().edit_group(group, name, loader, version, force)
    get_group_model().save()


def search(query: str, index: str = 'relevance', offset: int = 0, limit: int = 10):
    response = get_api_model().search_mod(query, index, offset, limit)

    table = Table("NAME", "SLUG", "AUTHOR", "CLIENT_SIDE", "SERVER_SIDE", "DOWNLOADS", box=box.HORIZONTALS)
    for project in response['hits']:
        table.add_row(project['title'], project['slug'], project['author'], project['client_side'], project['server_side'], str(project['downloads']))

    Console().print(table)