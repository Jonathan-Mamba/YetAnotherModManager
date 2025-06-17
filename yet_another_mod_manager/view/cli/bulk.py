import rich.markdown
import os
import subprocess
from rich.table import Table
from rich.console import Console
from rich import box
from yet_another_mod_manager.model import get_group_model, get_api_model
from yet_another_mod_manager.config import ModGroup
from yet_another_mod_manager.util.enums import ModLoader, MinecraftVersion
from tempfile import NamedTemporaryFile


def add(name: str, loader: ModLoader, version: MinecraftVersion):
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
        table.add_row(group.name, group.mod_loader, group.version, str(len(group.mods)))

    Console().print(table)


def edit(group_name: str, force: bool = False) -> None:
    path: str = ""
    group = get_group_model().get_group(group_name)
    with NamedTemporaryFile('w', delete_on_close=False, delete=False) as f:
        f.write("[GROUP_INFO]\n")
        f.write(f"NAME={group.name}\n")
        f.write(f"LOADER={group.mod_loader}\n")
        f.write(f"VERSION={group.version}\n\n")
        f.write("[MODS]\n")
        path = f.name

        for mod in group.mods:
            f.write(f"- {mod}\n")

    text_editors: list[str] = [os.environ.get(i) for i in ('EDITOR', 'nano', 'vim', 'notepad') if os.environ.get(i) is not None]
    if not text_editors:
        raise ValueError("could not find a text editor")

    subprocess.call([text_editors[0], path])

    #get_group_model().edit_group(group_name, name, loader, version, force)
    get_group_model().save()


def search(query: str, index: str = 'relevance', offset: int = 0, limit: int = 10):
    response = get_api_model().search_mod(query, index, offset, limit)

    table = Table("NAME", "SLUG", "AUTHOR", "CLIENT_SIDE", "SERVER_SIDE", "DOWNLOADS", box=box.HORIZONTALS)
    for project in response['hits']:
        table.add_row(project['title'], project['slug'], project['author'], project['client_side'],
                      project['server_side'], f"{project['downloads']:,}")

    Console().print(table)


def print_group(group_name: str):
    group = get_group_model().get_group(group_name)
    group_string = ""

    group_string += f"- NAME: '{group.name}'\n"
    group_string += f"- LOADER: '{group.mod_loader}'\n"
    group_string += f"- VERSION: '{group.version}'\n"
    group_string += f"- MODS:\n\t- "
    group_string += "\n\t- ".join(f"'{i}'" for i in group.mods)

    md = rich.markdown.Markdown(group_string)
    Console().print(md)
