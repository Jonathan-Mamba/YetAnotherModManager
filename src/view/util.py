import typer
from typing import Self
from src.model import get_model
from src import util
import pynput
import colorama

class App(typer.Typer, metaclass=util.MetaSingleton):
    """
    Singleton class that contains a reference to the app
    """
    def __init__(self):
        super().__init__(no_args_is_help=True)



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
