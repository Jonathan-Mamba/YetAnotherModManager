from typing import TypedDict, Literal


modloaders: tuple[str, str, str, str] = "fabric", "forge", "neoforge", "quilt"


class ModGroup(TypedDict):
    mod_loader: Literal["fabric", "forge", "neoforge", "quilt"]
    version: str
    name: str
    mods: list[str]

class ConfigFile(TypedDict):
    groups: list[ModGroup]



class MetaSingleton(type):
    __instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances.keys():
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]


if __name__ == '__main__':
    import pynput
    import time
    pressed = False
    stop = False
    def on_press(key):
        global pressed, stop
        if key == pynput.keyboard.Key.shift_l:
            pressed = True
        if key == pynput.keyboard.KeyCode.from_char("q"):
            stop = True



    listener = pynput.keyboard.Listener(on_press)
    listener.start()
    while True:
        if pressed:
            print(f"\rline\nmessa", end="")
            pressed = False
        if stop:
            print("\r ")
            break
    print("q")