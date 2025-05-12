import abc
import time
import argparse
import util
import pynput
import argparse
import colorama
from model import Model


def get_parser() -> tuple[argparse.ArgumentParser, dict[str, argparse.ArgumentParser]]:
    parser = argparse.ArgumentParser(prog="minecaft-mod-config", description="command parser", exit_on_error=False)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list", help="lists all local groups", exit_on_error=False)
    subparsers.add_parser("quit", help="terminates the program", exit_on_error=False)
    subparsers.add_parser("clear", help="clears the screen", exit_on_error=False)

    help_parser = subparsers.add_parser("help", help="shows this help message an", exit_on_error=False)
    help_parser.add_argument("sub_command", default="")

    add_parser = subparsers.add_parser("add", help="Adds a new group", exit_on_error=False)
    add_parser.add_argument("-n", "--name", help="Name of the new group", required=True)
    add_parser.add_argument("-l", "--loader", help="modloader of the new group", required=True)
    add_parser.add_argument("-v", "--version", help="version of the new group", required=True)

    remove_parser = subparsers.add_parser("remove", help="Removes an existing group", exit_on_error=False)
    remove_parser.add_argument("group", help="name of the group to be removed")

    edit_parser = subparsers.add_parser("edit", help="edit an existing group", exit_on_error=False)
    edit_parser.add_argument("group", help="name of the group to be edited")

    install_parser = subparsers.add_parser("install", help="installs the specified group", exit_on_error=False)
    install_parser.add_argument("-g", "--group", type=str, help="Name of the group to be installed", required=True)
    install_parser.add_argument("-d", "--destination", help="folder to install the group", required=True)

    search_parser = subparsers.add_parser("search", help="searches groups by name, mod_loader, and/or version", exit_on_error=False)
    search_parser.add_argument("-n", "--name", help="name of the searched group")
    search_parser.add_argument("-l", "--loader", help="loader of the searched group")
    search_parser.add_argument("-v", "--version", help="version of the searched group")
    return parser, subparsers._name_parser_map



class Stream:
    def __init__(self):
        self.quits: bool = False
        self.continues: bool = False

    def print_line(self, line: str) -> bool:
        self.quits, self.continues = False, False
        listener = pynput.keyboard.Listener(self.on_press)
        listener.start()
        print(
            f"\r{line}" + " " * max(0, 37-len(line)) + f"\n{colorama.Back.WHITE}{colorama.Fore.BLACK}Press SPACE to continue and Q to quit{colorama.Fore.RESET}{colorama.Back.RESET}",
            end="")
        while True:
            if self.quits:
                print()
                return False
            elif self.continues:
                return True

    def on_press(self, key):
        if key == pynput.keyboard.KeyCode.from_char("q"):
            self.quits = True
        elif key == pynput.keyboard.Key.space:
            self.continues = True



class View(abc.ABC):
    def __init__(self, model: Model):
        self.model = model


class CommandLineView(View):
    def execute(self, command: list[str]) -> str:
        if command[0] == "help" and len(command) == 1:
            return self.show_help("")

        args = get_parser()[0].parse_args(command)
        if args.command == "add":
            return self.add(args)
        elif args.command == "remove":
            return self.remove(args)
        elif args.command == "edit":
            return self.edit(args)
        elif args.command == "install":
            return self.install(args)
        elif args.command == "list":
            return self.list_groups(args)
        elif args.command == "search":
            return self.search(args)
        elif args.command == "help":
            return self.show_help(args.sub_command)
        elif args.command == "clear":
            return self.clear_screen()

        raise argparse.ArgumentError(None, message=f"'{command[0]}' is not a valid subcommand")

    def add(self, args: argparse.Namespace) -> str:
        self.model.add_group(util.ModGroup(mod_loader=args.loader, version=args.version, mods=[], name=args.name))
        return f"Group {args.name} was created successfully."

    def clear_screen(self) -> str:
        self.model.clear_screen()
        return ""

    def remove(self, args: argparse.Namespace) -> str:
        self.model.remove_group(args.group)
        return f"Group {args.group} was removed successfully."

    def edit(self, args: argparse.Namespace) -> str:
        return "edit command ran"

    def install(self, args: argparse.Namespace) -> str:
        return f"install command executed with {args}"

    def search(self, args: argparse.Namespace) -> str:
        return f"search command executed with {args}"

    def show_help(self, command: str) -> str:
        if command == "":
            get_parser()[0].print_help()
        else:
            try:
                get_parser()[1][command].print_help()
            except KeyError:
                raise argparse.ArgumentError(None, f"{command} is not a recognised command")
        return ""

    def list_groups(self, args: argparse.Namespace) -> str:
        stream = Stream()
        for group in self.model.get_groups():
            finished = not stream.print_line(f"GROUP {group['name']} ({group["mod_loader"]} {group["version"]}):")
            if finished:
                return ""
            for mod in group['mods']:
                finished = not stream.print_line(f"- {mod}")
                if finished:
                    return ""
        return ""



    def run(self):
        print("CLI client made to manage minecraft mods.\nType 'help' to get more info")
        while True:
            command = input(f"{colorama.Fore.GREEN}> {colorama.Fore.RESET}").split(" ")
            if command[0] == "":
                continue
            if command[0] == "quit":
                self.model.save()
                break
            try:
                print(self.execute(command))
            except argparse.ArgumentError as e:
                print(f"ERROR: {e}")
            """
            except Exception as e:
                print(f"FATAL ({type(e)}): {e}")
                quit(1)
            """