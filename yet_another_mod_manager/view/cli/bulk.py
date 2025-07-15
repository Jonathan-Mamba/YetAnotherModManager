import yaml
import subprocess
import rich.markdown
from rich import box
from rich.table import Table
from rich.console import Console
from tempfile import NamedTemporaryFile
from yet_another_mod_manager.model import get_group_model, get_api_model
from yet_another_mod_manager.config import ModGroup, Mod
from yet_another_mod_manager.util import get_text_editor, CommandError
from yet_another_mod_manager.util.enums import ModLoader, MinecraftVersion



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
        f.write(f"name: {group.name}\n")
        f.write(f"mod_loader: {group.mod_loader}\n")
        f.write(f"version: {group.version}\n")
        f.write("mods:")
        path = f.name

        for mod in group.mods:
            f.write(f"\n  - {mod.slug}")

    subprocess.call([get_text_editor(), path])
    with open(path) as f:
        data = yaml.load(f, yaml.Loader)

    if data is None:
        raise CommandError("Invalid file format")
    
    with open(path) as f:
        string = f.read()

    for line in string.splitlines():
        try: line.index('version')
        except ValueError: pass
        else: data['version'] = line.split(':')[1].strip()

    get_group_model().edit_group(ModGroup(data['name'], data['mod_loader'], data['version'], [Mod(i) for i in data['mods']]), group_name, force)
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
    group_string += f"- MODS:"

    for mod in group.mods:
        group_string += f"\n\t- '{mod.slug}'"
        group_string += f"\n\t\t- PLATFORM: '{mod.platform}'"
        group_string += f"\n\t\t- VERSION: '{mod.version}'"
        group_string += f"\n\t\t- CHANNEL: '{mod.channel}'\n"

    md = rich.markdown.Markdown(group_string)
    Console().print(md)


def config():
    subprocess.call([get_text_editor(), get_group_model().get_config_file_path()])